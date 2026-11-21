import json
import os
import time
import urllib.request
import urllib.parse
from collections import deque

OUTPUT_FILE = "data/songs.json"

# Start with K-Pop, J-Pop, C-Pop artists + a few Western ones
SEED_ARTISTS = [
    "BTS", "BLACKPINK", "Stray Kids", "TWICE", "SEVENTEEN", "IU", 
    "NewJeans", "aespa", "LE SSERAFIM", "EXO", "Girls' Generation",
    "YOASOBI", "Kenshi Yonezu", "Ado", "Official HIGE DANdism", 
    "Jay Chou", "JJ Lin", "G.E.M.", "Taylor Swift", "Drake"
]
MAX_ARTISTS_TO_CRAWL = 100 

def api_call(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'SongRecommenderProject/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  API Error: {e}")
        return None

def search_artist_tracks(artist_name):
    """
    Instead of looking up albums, we search for the artist's name directly.
    This pulls in EVERY track where they are the main artist or a feature.
    """
    tracks = []
    # Get up to 1000 tracks in batches of 100 (Deezer's max per page)
    for index in range(0, 1000, 100):
        url = f"https://api.deezer.com/search?q=artist:\"{urllib.parse.quote(artist_name)}\"&limit=100&index={index}"
        data = api_call(url)
        
        if not data or not data.get("data"):
            break # No more results
            
        for item in data["data"]:
            title = item.get("title", "").strip()
            artist = item.get("artist", {}).get("name", "").strip()
            cover = item.get("album", {}).get("cover_medium", "")
            
            # Only keep it if the artist name actually matches (avoids weird search bleed)
            if title and artist and (artist_name.lower() in artist.lower()):
                tracks.append({
                    "title": title,
                    "artist": artist,
                    "genre": artist_name, # Use main artist as genre proxy
                    "cover": cover
                })
        
        # Small pause between pages to not spam
        time.sleep(0.2)
        
        # If we got fewer than 100 results, we've reached the end
        if len(data["data"]) < 100:
            break
            
    return tracks

def get_related_artists(artist_name):
    """Find related artists using the first search result's ID."""
    url = f"https://api.deezer.com/search/artist?q={urllib.parse.quote(artist_name)}&limit=1"
    data = api_call(url)
    if data and data.get("data"):
        artist_id = data["data"][0]["id"]
        related_url = f"https://api.deezer.com/artist/{artist_id}/related?limit=10"
        rel_data = api_call(related_url)
        if rel_data and rel_data.get("data"):
            return [item["name"] for item in rel_data["data"]]
    return []

def main():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            songs = json.load(f)
    else:
        songs = []

    existing_keys = set((s["title"].lower(), s["artist"].lower()) for s in songs)
    initial_count = len(songs)
    
    artist_queue = deque(SEED_ARTISTS)
    visited_artists = set()
    artists_crawled = 0

    print(f"Starting deep search crawl with {len(songs)} existing songs...")

    while artist_queue and artists_crawled < MAX_ARTISTS_TO_CRAWL:
        current_artist = artist_queue.popleft()
        
        if current_artist.lower() in visited_artists:
            continue
            
        print(f"[{artists_crawled+1}/{MAX_ARTISTS_TO_CRAWL}] Crawling: {current_artist}...")
        
        # Get ALL tracks by this artist
        tracks = search_artist_tracks(current_artist)
        
        added = 0
        for track in tracks:
            key = (track["title"].lower(), track["artist"].lower())
            if key not in existing_keys:
                new_id = f"s{len(songs) + 1:06d}"
                songs.append({
                    "id": new_id,
                    "title": track["title"],
                    "artist": track["artist"],
                    "genre": track["genre"],
                    "cover": track["cover"]
                })
                existing_keys.add(key)
                added += 1
        
        print(f"  Found {len(tracks)} tracks, added {added} new songs.")
        visited_artists.add(current_artist.lower())
        
        # Find related artists to keep the chain going
        related = get_related_artists(current_artist)
        for r in related:
            if r.lower() not in visited_artists and r.lower() not in artist_queue:
                artist_queue.append(r)
                
        artists_crawled += 1
        
        # Auto-save every 5 artists
        if artists_crawled % 5 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(songs, f, indent=4, ensure_ascii=False)
            print(f"  [Auto-Saved. Total songs now: {len(songs)}]")
            
        time.sleep(0.5)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)
    
    print(f"\nCrawl finished! Total songs: {len(songs)} (Started with {initial_count})")

if __name__ == "__main__":
    main()