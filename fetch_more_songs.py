import json
import os
import time
import urllib.request
import urllib.parse

OUTPUT_FILE = "data/songs.json"

# A much larger list of artists across different eras and genres
ARTIST_LIST = [
    "TNT", "TFBOYS", "Taylor Swift", "Drake", "The Weeknd", "Ed Sheeran", "Billie Eilish",
    "Queen", "Eminem", "Adele", "Bruno Mars", "Coldplay", "Rihanna",
    "Kanye West", "Beyoncé", "Kendrick Lamar", "Ariana Grande", "Post Malone",
    "Dua Lipa", "Harry Styles", "Justin Bieber", "Bad Bunny", "BTS",
    "Michael Jackson", "Madonna", "Elton John", "David Bowie", "Prince",
    "Fleetwood Mac", "Nirvana", "Metallica", "AC/DC", "Guns N' Roses",
    "Bob Marley", "Johnny Cash", "Dolly Parton", "Frank Sinatra", "Miles Davis",
    "Daft Punk", "Calvin Harris", "David Guetta", "Marshmello", "Avicii",
    # Add 50-100 more artists here for even more data
]

def fetch_artist_top_tracks(artist_name, limit=70):
    """Fetch top tracks for a specific artist."""
    tracks = []
    # Use the artist search to get their ID, then get their top tracks
    search_url = f"https://api.deezer.com/search/artist?q={urllib.parse.quote(artist_name)}&limit=1"
    
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'SongRecommenderProject/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data.get("data"):
                return []
            artist_id = data["data"][0]["id"]
        
        # Now get the artist's top tracks
        top_url = f"https://api.deezer.com/artist/{artist_id}/top?limit={limit}"
        req = urllib.request.Request(top_url, headers={'User-Agent': 'SongRecommenderProject/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            for item in data.get("data", []):
                title = item.get("title", "").strip()
                artist = item.get("artist", {}).get("name", "").strip()
                # Use the artist name as the "genre" proxy for now
                genre = artist_name 
                
                if title and artist:
                    tracks.append({"title": title, "artist": artist, "genre": genre})
    except Exception as e:
        print(f"  Error fetching '{artist_name}': {e}")
        
    return tracks

def main():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            songs = json.load(f)
    else:
        songs = []
    
    existing_keys = set((s["title"].lower(), s["artist"].lower()) for s in songs)
    initial_count = len(songs)
    
    for artist in ARTIST_LIST:
        print(f"Fetching top tracks for: {artist}...")
        new_tracks = fetch_artist_top_tracks(artist, limit=50)
        
        added = 0
        for track in new_tracks:
            key = (track["title"].lower(), track["artist"].lower())
            if key not in existing_keys:
                new_id = f"s{len(songs) + 1:06d}"
                songs.append({
                    "id": new_id,
                    "title": track["title"],
                    "artist": track["artist"],
                    "genre": track["genre"]
                })
                existing_keys.add(key)
                added += 1
        
        print(f"  Added {added} new songs.")
        time.sleep(1.5)  # Respect rate limit

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)
    
    print(f"\nDone! Total songs: {len(songs)} (was {initial_count})")

if __name__ == "__main__":
    main()