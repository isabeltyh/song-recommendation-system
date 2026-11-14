"""
Convert the Kaggle songs CSV into data/songs.json.

Dataset: waqi786/songs-dataset-2000-2020-50k-records
Columns in CSV: Title, Artist, Album, Genre, Release Date, Duration, Popularity
We keep only Title, Artist, Genre — the fields needed for content-based filtering.

Usage:
    python src/load_kaggle.py path/to/songs_2000_2020_50k.csv
"""
import csv
import json
import os
import sys


def convert(csv_path: str, out_path: str = "data/songs.json"):
    songs = []
    seen = set()

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            # Exact column names as published on Kaggle
            title = (row.get("Title") or "").strip()
            artist = (row.get("Artist") or "").strip()
            genre = (row.get("Genre") or "").strip()

            # Skip rows missing any required field
            if not title or not artist or not genre:
                continue

            # De-duplicate on (title, artist) case-insensitively
            key = (title.lower(), artist.lower())
            if key in seen:
                continue
            seen.add(key)

            songs.append({
                "id": f"s{i:05d}",
                "title": title,
                "artist": artist,
                "genre": genre,
            })

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)

    print(f"Wrote {len(songs)} unique songs to {out_path}")

    # Show genre distribution for a sanity check
    from collections import Counter
    counts = Counter(s["genre"] for s in songs)
    print("\nGenre distribution:")
    for g, c in counts.most_common():
        print(f"  {g}: {c}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/load_kaggle.py path/to/songs_2000_2020_50k.csv")
        sys.exit(1)
    convert(sys.argv[1])