"""
fix_genres.py (Updated)
Replaces artist-name-as-genre with real genres and fills in duration/popularity.
Uses a manual map for speed, then Deezer's search API for the rest.
"""
import json
import os
import time
import urllib.request
import urllib.parse

OUTPUT_FILE = "data/songs.json"

# --- Manual genre mapping for popular artists ---
GENRE_MAP = {
    "taylor swift": "Pop", "ed sheeran": "Pop", "adele": "Pop",
    "billie eilish": "Pop", "dua lipa": "Pop", "harry styles": "Pop",
    "bruno mars": "Pop", "ariana grande": "Pop", "justin bieber": "Pop",
    "bts": "K-Pop", "blackpink": "K-Pop", "stray kids": "K-Pop",
    "twice": "K-Pop", "seventeen": "K-Pop", "iu": "K-Pop",
    "jungkook": "K-Pop", "newjeans": "K-Pop", "aespa": "K-Pop",
    "le sserafim": "K-Pop", "exo": "K-Pop", "girls' generation": "K-Pop",
    "drake": "Hip-Hop", "kanye west": "Hip-Hop", "kendrick lamar": "Hip-Hop",
    "eminem": "Hip-Hop", "post malone": "Hip-Hop", "travis scott": "Hip-Hop",
    "queen": "Rock", "coldplay": "Rock", "nirvana": "Rock",
    "metallica": "Rock", "ac/dc": "Rock", "guns n' roses": "Rock",
    "the weeknd": "R&B", "beyoncé": "R&B", "rihanna": "R&B",
    "frank ocean": "R&B",
    "daft punk": "Electronic", "calvin harris": "Electronic",
    "avicii": "Electronic", "marshmello": "Electronic", "david guetta": "Electronic",
    "yoasobi": "J-Pop", "kenshi yonezu": "J-Pop", "ado": "J-Pop",
    "official hige dandism": "J-Pop",
    "jay chou": "C-Pop", "jj lin": "C-Pop", "g.e.m.": "C-Pop",
    "jackson wang": "C-Pop",
}

def api_call(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'SongRecommenderProject/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def lookup_track_metadata(title, artist):
    """
    Searches Deezer for a specific track, then fetches its details.
    Returns: dict with 'genre', 'duration', 'popularity' (or None for any field).
    """
    # 1. Search for the track
    query = f"{artist} {title}"
    search_url = f"https://api.deezer.com/search?q={urllib.parse.quote(query)}&limit=1"
    data = api_call(search_url)
    
    if not data or not data.get("data"):
        return None
    
    track = data["data"][0]
    track_id = track["id"]
    
    # 2. Get detailed track info (includes duration, rank)
    details_url = f"https://api.deezer.com/track/{track_id}"
    details = api_call(details_url)
    
    if not details:
        return None
    
    result = {}
    
    # Duration in seconds
    result["duration_seconds"] = details.get("duration", 0)
    
    # Popularity / Rank (0-1000000, we normalize to 0-100)
    rank = details.get("rank", 0)
    result["popularity"] = min(100, round(rank / 10000))
    
    # Genre: get from album, then look up the genre name
    album_id = details.get("album", {}).get("id")
    if album_id:
        album_details = api_call(f"https://api.deezer.com/album/{album_id}")
        if album_details:
            genre_id = album_details.get("genre_id", 0)
            if genre_id and genre_id != 0:
                genre_data = api_call(f"https://api.deezer.com/genre/{genre_id}")
                if genre_data and genre_data.get("name"):
                    result["genre"] = genre_data["name"]
    
    return result

def main():
    if not os.path.exists(OUTPUT_FILE):
        print("No songs.json found.")
        return

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        songs = json.load(f)

    # Find songs that need any of the 3 fields fixed:
    # - genre is the artist name (placeholder)
    # - duration_seconds is missing
    # - popularity is missing
    to_fix = [
        s for s in songs
        if s.get("genre", "").strip().lower() == s.get("artist", "").strip().lower()
        or "duration_seconds" not in s
        or "popularity" not in s
    ]
    print(f"Found {len(to_fix)} songs needing metadata. Fetching from Deezer...")

    fixed_count = 0
    for i, song in enumerate(to_fix):
        title = song["title"]
        artist = song["artist"]
        
        print(f"[{i+1}/{len(to_fix)}] {title} by {artist}...")

        # Try the manual map first (only for genre)
        manual_genre = GENRE_MAP.get(artist.strip().lower())
        if manual_genre and song.get("genre", "").strip().lower() == artist.strip().lower():
            song["genre"] = manual_genre

        # If we still need duration/popularity, hit the API
        needs_api = (
            "duration_seconds" not in song or
            "popularity" not in song or
            (song.get("genre", "").strip().lower() == artist.strip().lower())
        )

        if needs_api:
            meta = lookup_track_metadata(title, artist)
            if meta:
                if "genre" in meta and song.get("genre", "").strip().lower() == artist.strip().lower():
                    song["genre"] = meta["genre"]
                if "duration_seconds" in meta:
                    song["duration_seconds"] = meta["duration_seconds"]
                if "popularity" in meta:
                    song["popularity"] = meta["popularity"]
                fixed_count += 1
            else:
                # Fallback if API fails
                if "duration_seconds" not in song:
                    song["duration_seconds"] = 0
                if "popularity" not in song:
                    song["popularity"] = 0
                if song.get("genre", "").strip().lower() == artist.strip().lower():
                    song["genre"] = "Unknown"
            
            time.sleep(0.3)  # Respect API rate limit

        # Save progress every 25 songs
        if (i + 1) % 25 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(songs, f, indent=4, ensure_ascii=False)
            print(f"  [Auto-Saved. Fixed {fixed_count} so far.]")

    # Final save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)

    print(f"\nDone! Fixed {fixed_count} songs with full metadata.")

if __name__ == "__main__":
    main()