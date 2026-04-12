"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# --- Standard profiles ---
profiles = {
    "Upbeat Pop Fan":          {"genre": "pop",     "mood": "happy",    "energy": 0.8,  "valence": 0.85},
    "Chill Indie Listener":    {"genre": "indie",   "mood": "chill",    "energy": 0.3,  "valence": 0.4},
    "High-Energy Hip-Hop Head":{"genre": "hip-hop", "mood": "energetic","energy": 0.95, "valence": 0.7},
}

# --- Adversarial / edge case profiles ---
# Each is designed to expose a specific weakness in the scoring logic.
adversarial_profiles = {
    # Genre (+25) + energy proximity can outscore mood match (+30) when energy is far off
    "High-Energy Sad Person":   {"genre": "metal", "mood": "sad",     "energy": 0.9, "valence": 0.2},

    # No song matches either tag — rankings collapse to energy/valence proximity only
    "Unknown Genre and Mood":   {"genre": "k-pop", "mood": "anxious", "energy": 0.5, "valence": 0.5},

    # "Pop"/"Happy" != "pop"/"happy" — case mismatch silently kills both bonuses
    "Case Sensitivity Trap":    {"genre": "Pop",   "mood": "Happy",   "energy": 0.8},

    # energy=1.5 is out of range; proximity scores become tiny, neutering the signal
    "Out-of-Range Energy":      {"genre": "pop",   "mood": "happy",   "energy": 1.5},

    # No lofi song is angry; partial genre match beats the mood the user asked for
    "Impossible Combo":         {"genre": "lofi",  "mood": "angry",   "energy": 0.6},

    # Works as expected — included as a control to confirm the logic isn't always broken
    "All-Neutral Profile":      {"genre": "ambient","mood": "chill",  "energy": 0.5, "valence": 0.5},
}


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 3) -> None:
    print(f"\n{'='*55}")
    print(f"  {name}")
    print(f"  Prefs: {user_prefs}")
    print(f"{'='*55}")
    try:
        results = recommend_songs(user_prefs, songs, k=k)
        for i, (song, score, explanation) in enumerate(results, start=1):
            print(f"\n  #{i}: {song['title']} by {song['artist']}")
            print(f"       Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
            print(f"       Score: {score:.1f} / 90")
            print(f"       Why  : {explanation}")
    except Exception as e:
        print(f"\n  !! CRASH: {type(e).__name__}: {e}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs")

    print("\n" + "#" * 55)
    print("  STANDARD PROFILES")
    print("#" * 55)
    for name, prefs in profiles.items():
        run_profile(name, prefs, songs)

    print("\n\n" + "#" * 55)
    print("  ADVERSARIAL PROFILES")
    print("#" * 55)
    for name, prefs in adversarial_profiles.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
