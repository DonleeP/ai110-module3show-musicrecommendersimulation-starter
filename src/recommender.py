import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# ---------------------------------------------------------------------------
# Algorithm Recipe (Phase 2)
# ---------------------------------------------------------------------------
# These weights ARE the recommender's "opinion" about what matters. Genre is
# the strongest taste signal, so it earns the most. Mood is a real but softer
# signal. Energy is a number (0.0-1.0), so instead of a yes/no point it earns
# partial credit that shrinks the further a song is from the target energy.
GENRE_WEIGHT = 2.0      # exact genre match
MOOD_WEIGHT = 1.0       # exact mood match
ENERGY_WEIGHT = 2.0     # max points when the song's energy equals the target
ACOUSTIC_WEIGHT = 1.0   # bonus when an acoustic-loving user gets an acoustic song
ACOUSTIC_THRESHOLD = 0.6  # a song counts as "acoustic" above this acousticness


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k songs that best match the user's profile, best first."""
        prefs = _profile_to_prefs(user)
        # Score every song, then keep the k highest. sort() is stable, so ties
        # keep the catalog's original order.
        scored = [(song, score_song(prefs, asdict(song))[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable sentence explaining why a song was recommended."""
        prefs = _profile_to_prefs(user)
        score, reasons = score_song(prefs, asdict(song))
        if reasons:
            return f"'{song.title}' scored {score:.1f} because it " + ", ".join(reasons) + "."
        return f"'{song.title}' scored {score:.1f} — recommended as a general pick."

def load_songs(csv_path: str) -> List[Dict]:
    """Read a songs CSV into a list of dicts, converting numeric columns to numbers."""
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user prefs, returning (score, reasons-with-points)."""
    score = 0.0
    reasons: List[str] = []

    # +2.0 for an exact genre match.
    if user_prefs.get("genre") and song.get("genre") == user_prefs["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.1f})")

    # +1.0 for an exact mood match.
    if user_prefs.get("mood") and song.get("mood") == user_prefs["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.1f})")

    # Energy similarity: full points when identical, scaling to 0 as the gap
    # approaches 1.0. Energy is on a 0.0-1.0 scale, so abs(diff) is at most 1.0.
    target_energy = user_prefs.get("energy")
    if target_energy is not None and song.get("energy") is not None:
        closeness = 1.0 - abs(float(song["energy"]) - float(target_energy))
        energy_points = ENERGY_WEIGHT * closeness
        score += energy_points
        reasons.append(f"energy match ({closeness * 100:.0f}% close) (+{energy_points:.1f})")

    # Optional acoustic bonus for users who set likes_acoustic.
    if user_prefs.get("likes_acoustic") and float(song.get("acousticness", 0.0)) >= ACOUSTIC_THRESHOLD:
        score += ACOUSTIC_WEIGHT
        reasons.append(f"acoustic bonus (+{ACOUSTIC_WEIGHT:.1f})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank every song, returning the top k as (song, score, explanation)."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "a general suggestion"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]

def _profile_to_prefs(user: UserProfile) -> Dict:
    """Bridges the OOP UserProfile to the dict shape score_song() expects."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }
