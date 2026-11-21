import json
import os
import time
import urllib.request
import urllib.parse
from collections import deque

OUTPUT_FILE = "data/songs.json"

# Start with a few diverse seed artists
SEED_ARTISTS = [
    
    # K-Pop (Global groups & soloists)
    "BTS", "BLACKPINK", "Stray Kids", "TWICE", "SEVENTEEN", "IU", "Jungkook",
    "NewJeans", "aespa", "LE SSERAFIM", "EXO", "Girls' Generation",
    
    # J-Pop (Popular artists & groups)
    "YOASOBI", "Kenshi Yonezu", "Ado", "Official HIGE DANdism", "LiSA", 
    "Fujii Kaze", "King Gnu", "Hikaru Utada", "Arashi",
    
    # C-Pop (Mandopop/Cantopop)
    "Jay Chou", "JJ Lin", "G.E.M.", "Hua Chenyu", "Jackson Wang", 
    "Teresa Teng", "Eason Chan", "Mayday", "Zhou Shen"
]
MAX_ARTISTS_TO_CRAWL = 100 # Lower this if it takes too long, raise it for more data

def api_call(url):
    """Helper to make a request to Deezer API."""
    req = urllib.request.Request(url, headers={'User-Agent': 'SongRecommenderProject/1.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  API Error: {e}")
        return None

def get_artist_id(artist_name):
    url = f"https://api.deezer.com/search/artist?q={urllib.parse.quote(artist_name)}&limit=1"
    data = api_call(url)
    if data and data.get("data"):
        return data["data"][0]["id"], data["data"][0]["name"]
    return None, None

def get_artist_albums(artist_id, limit=100):
    """Get all albums for an artist, including cover images."""
    url = f"https://api.deezer.com/artist/{artist_id}/albums?limit={limit}"
    data = api_call(url)
    albums = []
    if data and data.get("data"):
        for item in data["data"]:
            albums.append({
                "id": item["id"],
                "cover_medium": item.get("cover_medium", "")
            })
    return albums

def get_album_tracks(album_id, artist_name, album_cover):
    """Get all tracks from a specific album."""
    url = f"https://api.deezer.com/album/{album_id}/tracks?limit=100"
    data = api_call(url)
    tracks = []
    if data and data.get("data"):
        for item in data["data"]:
            title = item.get("title", "").strip()
            if title:
                tracks.append({
                    "title": title,
                    "artist": artist_name,
                    "genre": artist_name,
                    "cover": album_cover
                })
    return tracks

def get_related_artists(artist_id):
    url = f"https://api.deezer.com/artist/{artist_id}/related?limit=10"
    data = api_call(url)
    related = []
    if data and data.get("data"):
        for item in data["data"]:
            related.append(item["name"])
    return related

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

    print(f"Starting deep album crawl with {len(songs)} existing songs...")

    while artist_queue and artists_crawled < MAX_ARTISTS_TO_CRAWL:
        current_artist = artist_queue.popleft()
        
        if current_artist.lower() in visited_artists:
            continue
            
        print(f"[{artists_crawled+1}/{MAX_ARTISTS_TO_CRAWL}] Crawling artist: {current_artist}...")
        
        artist_id, official_name = get_artist_id(current_artist)
        if not artist_id:
            continue
            
        visited_artists.add(current_artist.lower())
        
        # Get all albums
        albums_data = get_artist_albums(artist_id)
        print(f"  Found {len(albums_data)} albums. Fetching tracks...")
        
        added = 0
        for album in albums_data:
            album_cover = album.get("cover_medium", "")
            tracks = get_album_tracks(album["id"], official_name, album_cover)
            
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
            # Small pause between albums
            time.sleep(0.2) 
        
        print(f"  Added {added} total songs for {official_name}.")
        
        # Find related artists
        related = get_related_artists(artist_id)
        for r in related:
            if r.lower() not in visited_artists:
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