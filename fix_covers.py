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
    except Exception as e:
        print(f"  API Error: {e}")
        return None

def get_cover_for_track(title, artist):
    """Search Deezer for a specific track to get its album cover."""
    # Construct a specific search query: artist + title
    query = f"{artist} {title}"
    url = f"https://api.deezer.com/search/track?q={urllib.parse.quote(query)}&limit=1"
    
    data = api_call(url)
    if data and data.get("data"):
        # Return the album cover from the first result
        return data["data"][0].get("album", {}).get("cover_medium", "")
    return ""

def main():
    if not os.path.exists(OUTPUT_FILE):
        print("No songs.json found.")
        return

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        songs = json.load(f)

    # Find songs that don't have a cover or have a very short/placeholder cover string
    missing_covers = [s for s in songs if not s.get("cover") or len(s.get("cover", "")) < 5]
    print(f"Found {len(missing_covers)} songs missing art. Fetching from Deezer...")

    updated_count = 0
    for i, song in enumerate(missing_covers):
        # To avoid hitting rate limits too hard, we process in small batches
        print(f"[{i+1}/{len(missing_covers)}] Fetching art for: {song['title']} by {song['artist']}")
        
        cover_url = get_cover_for_track(song["title"], song["artist"])
        if cover_url:
            song["cover"] = cover_url
            updated_count += 1
        
        # Deezer rate limit: 50 requests per 5 seconds.
        # A small sleep keeps us safe. [citation:3][citation:15]
        time.sleep(0.2)

        # Save progress every 20 songs so we don't lose work
        if (i + 1) % 20 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(songs, f, indent=4, ensure_ascii=False)
            print(f"  [Auto-Saved. Updated {updated_count} covers so far.]")

    # Final save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)

    print(f"\nDone! Successfully added art for {updated_count} songs.")

if __name__ == "__main__":
    main()