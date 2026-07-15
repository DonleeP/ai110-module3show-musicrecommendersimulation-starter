"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# A suite of user profiles for stress-testing the recommender.
# The first three are "normal" diverse tastes; the last three are adversarial
# edge cases designed to try to trick the scoring logic.
PROFILES = [
    ("High-Energy Pop",          {"genre": "pop", "mood": "happy", "energy": 0.9}),
    ("Chill Lofi",               {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}),
    ("Deep Intense Rock",        {"genre": "rock", "mood": "intense", "energy": 0.9}),
    # --- Adversarial / edge cases ---
    ("Conflicting: Sad + Hyper", {"genre": "pop", "mood": "melancholic", "energy": 0.95}),
    ("Genre Not in Catalog",     {"genre": "kpop", "mood": "happy", "energy": 0.7}),
    ("Mood Only (no genre)",     {"mood": "chill", "energy": 0.5}),
]


def print_recommendations(label: str, user_prefs: dict, songs: list) -> None:
    """Run the recommender for one profile and print the top 5 in a clean layout."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 60)
    print(f"🎵  PROFILE: {label}")
    print("=" * 60)
    prefs_line = "  |  ".join(f"{key}={value}" for key, value in user_prefs.items())
    print(f"Your profile:  {prefs_line}")
    print(f"\nTop {len(recommendations)} recommendations:\n")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES:
        print_recommendations(label, user_prefs, songs)


if __name__ == "__main__":
    main()
