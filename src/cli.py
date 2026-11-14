"""
Command-Line Interface for Song Recommendation System.
"""
from src.song_recommender import SongRecommender


def main():
    rec = SongRecommender()
    print("=" * 55)
    print("Song Recommendation System")
    print("=" * 55)
    print("Available genres:", ", ".join(rec.get_all_genres()))

    title = input("\nEnter a song title: ").strip()
    genre = input("Genre filter (or 'all'): ").strip() or "all"
    count_raw = input("How many recommendations? ").strip()

    try:
        count = int(count_raw)
    except ValueError:
        print("\nError: recommendation count must be a whole number.")
        return

    result = rec.recommend(title, genre, count)

    if not result["success"]:
        print(f"\nError: {result['error']}")
        return

    if not result["results"]:
        print("\nNo matching songs found. Try 'all' genres.")
        return

    print(f"\nTop {len(result['results'])} recommendation(s):")
    for i, s in enumerate(result["results"], 1):
        print(f"{i}. {s['title']} — {s['artist']} ({s['genre']})")
        print(f"   Score: {s['score']}/100 | {s['explanation']}")

    if result["note"]:
        print(f"\nNote: {result['note']}")


if __name__ == "__main__":
    main()