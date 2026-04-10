import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    target_valence: float
    likes_acoustic: bool = False

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs recommended for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
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
    return songs

def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Score a song against user preferences and return the score with an explanation."""
    score = 0.0
    reasons = []

    if song["mood"] == user_prefs["mood"]:
        score += 30
        reasons.append(f"mood match (+30)")

    if song["genre"] == user_prefs["genre"]:
        score += 25
        reasons.append(f"genre match (+25)")

    energy_pts = (1 - abs(song["energy"] - user_prefs["energy"])) * 20
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.1f})")

    valence_pts = (1 - abs(song["valence"] - user_prefs.get("valence", 0.5))) * 15
    score += valence_pts
    reasons.append(f"valence proximity (+{valence_pts:.1f})")

    explanation = ", ".join(reasons)
    return score, explanation

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(song, user_prefs)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
