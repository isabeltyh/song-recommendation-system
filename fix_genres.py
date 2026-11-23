import json
import os
import time
import urllib.request
import urllib.parse

OUTPUT_FILE = "data/songs.json"

def api_call(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'SongRecommenderProject/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def get_artist_genre(artist_name):
    """Search for the artist, get their ID, then look up their albums to find a genre."""
    # 1. Get the artist ID
    search_url = f"https://api.deezer.com/search/artist?q={urllib.parse.quote(artist_name)}&limit=1"
    data = api_call(search_url)
    if not data or not data.get("data"):
        return None
        
    artist_id = data["data"][0]["id"]
    
    # 2. Get the artist's albums
    album_url = f"https://api.deezer.com/artist/{artist_id}/albums?limit=5"
    album_data = api_call(album_url)
    
    if album_data and album_data.get("data"):
        for album in album_data["data"]:
            # Deezer albums have a "genre_id", but they don't return the genre name directly.
            # We have to look up the genre_id using the genre endpoint.
            genre_id = album.get("genre_id")
            if genre_id and genre_id != 0:
                # Deezer's genre IDs: 132 = Pop, 152 = Rock, 116 = Rap/Hip Hop, etc.
                # We can fetch the genre name.
                genre_url = f"https://api.deezer.com/genre/{genre_id}"
                genre_data = api_call(genre_url)
                if genre_data and genre_data.get("name"):
                    return genre_data["name"]
                    
    return None

def main():
    if not os.path.exists(OUTPUT_FILE):
        print("No songs.json found.")
        return

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        songs = json.load(f)

    # Find songs where the genre is exactly the artist name (our placeholder)
    to_fix = [s for s in songs if s.get("genre", "").strip().lower() == s.get("artist", "").strip().lower()]
    print(f"Found {len(to_fix)} songs with missing genres. Looking them up on Deezer...")

    # Create a cache so we don't look up the same artist 100 times
    artist_genre_cache = {}
    updated_count = 0

    for i, song in enumerate(to_fix):
        artist = song["artist"]
        
        if artist in artist_genre_cache:
            genre = artist_genre_cache[artist]
        else:
            print(f"[{i+1}/{len(to_fix)}] Looking up genre for: {artist}")
            genre = get_artist_genre(artist)
            # Save to cache (even if None) to avoid repeat lookups
            artist_genre_cache[artist] = genre
            time.sleep(0.3) # Respect API limits
            
        if genre:
            song["genre"] = genre
            updated_count += 1

    # Save back to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)

    print(f"\nDone! Updated {updated_count} songs with real genres.")

if __name__ == "__main__":
    main()