"""
Song Recommendation Engine
Content-based filtering on artist + genre, with genre pre-filtering,
similarity scoring, input validation, adjustable count, and explanations.

Adapted from the starter StudyRecommender structure.
"""

import json
import os
from typing import Dict, List, Tuple


class SongRecommender:
    """
    Content-based song recommender.

    Similarity scoring:
      - Artist match: ARTIST_WEIGHT (primary signal)
      - Genre match:  GENRE_WEIGHT  (secondary signal)
      Weights sum to 100 so the score is directly user-facing (0-100).
    """

    ARTIST_WEIGHT = 70
    GENRE_WEIGHT = 30

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.songs: List[Dict] = []
        self.load_data()

    # ---------- Loading ----------

    def load_data(self):
        path = os.path.join(self.data_dir, "songs.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Songs file not found: {path}")
        with open(path, "r") as f:
            self.songs = json.load(f)

    # ---------- Lookup ----------

    def find_song_by_title(self, title: str) -> Dict:
        """Case-insensitive exact title match."""
        target = title.strip().lower()
        for song in self.songs:
            if song["title"].strip().lower() == target:
                return song
        return None

    def get_all_genres(self) -> List[str]:
        return sorted({s["genre"] for s in self.songs})

    # ---------- Similarity ----------

    def _similarity(self, base: Dict, candidate: Dict) -> Tuple[float, List[str]]:
        """Return (score 0-100, explanation fragments)."""
        score = 0.0
        reasons = []

        if candidate["artist"].strip().lower() == base["artist"].strip().lower():
            score += self.ARTIST_WEIGHT
            reasons.append(f"same artist ({base['artist']})")

        if candidate["genre"].strip().lower() == base["genre"].strip().lower():
            score += self.GENRE_WEIGHT
            reasons.append(f"same genre ({base['genre']})")

        return score, reasons

    # ---------- Main entry point ----------

    def recommend(self, song_title: str, genre: str = "all", count: int = 5) -> Dict:
        """
        Return dict:
          {
            "success": bool,
            "error":   str | None,
            "results": [ {song fields..., score, explanation} ],
            "note":    str | None
          }
        """
        # --- Validation (Modification 2) ---
        if not isinstance(count, int) or count <= 0:
            return {
                "success": False, "results": [],
                "error": "Recommendation count must be a positive whole number.",
                "note": None,
            }

        base = self.find_song_by_title(song_title)
        if base is None:
            return {
                "success": False, "results": [],
                "error": f"Song '{song_title}' was not found in the dataset.",
                "note": None,
            }

        # --- Genre filter (Modification 1) ---
        if genre and genre.lower() != "all":
            if genre.lower() not in {g.lower() for g in self.get_all_genres()}:
                return {
                    "success": False, "results": [],
                    "error": f"Unknown genre '{genre}'. Available: "
                             f"{', '.join(self.get_all_genres())}.",
                    "note": None,
                }
            candidates = [s for s in self.songs
                          if s["genre"].lower() == genre.lower()]
        else:
            candidates = list(self.songs)

        # --- Score & rank ---
        scored = []
        for song in candidates:
            if song["id"] == base["id"]:
                continue  # exclude the selected song itself
            score, reasons = self._similarity(base, song)
            if score > 0:
                scored.append((song, score, reasons))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:count]

        results = []
        for song, score, reasons in top:
            explanation = ("Matches " + " and ".join(reasons)) if reasons \
                          else "Similar genre/artist profile"
            results.append({**song, "score": round(score, 1),
                            "explanation": explanation})

        note = None
        if len(results) < count:
            note = (f"Only {len(results)} matching song(s) available "
                    f"(requested {count}).")

        return {"success": True, "error": None,
                "results": results, "note": note}