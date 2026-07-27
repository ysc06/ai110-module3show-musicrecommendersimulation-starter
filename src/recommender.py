import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py

    Note: `danceability` is not present in data/songs.csv, so it defaults
    here. This lets a Song be built from the CSV data while the tests, which
    pass danceability explicitly, keep working.
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float = 0.5
    acousticness: float = 0.0

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


# ---------------------------------------------------------------------------
# Scoring configuration
#
# Design principle: no single soft signal should overturn a hard-identity
# match. Genre is the anchor (highest weight); mood, energy, and acoustic
# texture only nudge from there.
#
# Positive signals sum to 100. The acoustic signal is signed, so the final
# score ranges roughly -10 .. 100.
# ---------------------------------------------------------------------------
GENRE_WEIGHT = 35
MOOD_WEIGHT = 30
ENERGY_WEIGHT = 25

ACOUSTIC_REWARD = 10      # likes acoustic AND song is acoustic
ACOUSTIC_MISS_PENALTY = -5    # wanted acoustic, song isn't (missing nice-to-have)
ACOUSTIC_UNWANTED_PENALTY = -10  # dislikes acoustic, but song is (active turn-off)

ACOUSTIC_THRESHOLD = 0.6  # acousticness above this counts as "an acoustic song"
MOOD_ADJACENT_FACTOR = 0.6  # partial credit for a related-but-not-exact mood

# Symmetric adjacency: moods that "feel close" earn partial mood credit.
# Lookups check both directions, so each edge only needs to be listed once.
MOOD_NEIGHBORS = {
    "focused": {"chill", "relaxed"},
    "chill": {"relaxed", "happy"},
    "happy": {"energetic", "hopeful"},
    "energetic": {"intense"},
    "relaxed": {"nostalgic"},
    "moody": {"melancholic", "nostalgic"},
    "melancholic": {"romantic"},
}


def _mood_subscore(mood_pref: str, song_mood: str) -> float:
    """1.0 for an exact mood match, MOOD_ADJACENT_FACTOR for an adjacent mood, else 0."""
    if song_mood == mood_pref:
        return 1.0
    if song_mood in MOOD_NEIGHBORS.get(mood_pref, set()) or \
       mood_pref in MOOD_NEIGHBORS.get(song_mood, set()):
        return MOOD_ADJACENT_FACTOR
    return 0.0


def _score_core(
    genre_pref: str,
    mood_pref: str,
    energy_target: float,
    likes_acoustic: bool,
    song_genre: str,
    song_mood: str,
    song_energy: float,
    song_acousticness: float,
) -> Tuple[float, List[str]]:
    """
    Shared scoring engine used by both the functional and OOP APIs.
    Returns (score, reasons) so callers can rank and explain.
    """
    score = 0.0
    reasons: List[str] = []

    # --- Genre: exact match, the identity anchor ---------------------------
    if song_genre == genre_pref:
        score += GENRE_WEIGHT
        reasons.append(f"matches your favorite genre ({genre_pref})")

    # --- Mood: graded via adjacency ----------------------------------------
    mood_sub = _mood_subscore(mood_pref, song_mood)
    if mood_sub == 1.0:
        score += MOOD_WEIGHT
        reasons.append(f"matches your mood ({mood_pref})")
    elif mood_sub > 0.0:
        score += MOOD_WEIGHT * mood_sub
        reasons.append(f"has a related mood ({song_mood} ~ {mood_pref})")

    # --- Energy: closeness to the target -----------------------------------
    energy_sub = max(0.0, 1.0 - abs(song_energy - energy_target))
    score += ENERGY_WEIGHT * energy_sub
    if energy_sub >= 0.8:
        reasons.append(f"energy {song_energy:.2f} is close to your target {energy_target:.2f}")

    # --- Acoustic: signed reward / penalty ---------------------------------
    is_acoustic = song_acousticness > ACOUSTIC_THRESHOLD
    if likes_acoustic and is_acoustic:
        score += ACOUSTIC_REWARD
        reasons.append("has the acoustic texture you enjoy")
    elif likes_acoustic and not is_acoustic:
        score += ACOUSTIC_MISS_PENALTY
        reasons.append("less acoustic than you prefer")
    elif not likes_acoustic and is_acoustic:
        score += ACOUSTIC_UNWANTED_PENALTY
        reasons.append("more acoustic than you like")

    if not reasons:
        reasons.append("no strong matches with your profile")

    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        return _score_core(
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            user.likes_acoustic,
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda s: self._score(user, s)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score(user, song)
        return f"Score {score:.1f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file, coercing numeric columns to numbers.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    float_cols = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song: Dict = {}
            for key, value in row.items():
                if key == "id":
                    song[key] = int(value)
                elif key in float_cols:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song (dict) against user preferences (dict).
    Returns (score, reasons).
    Required by recommend_songs() and src/main.py
    """
    return _score_core(
        user_prefs.get("genre", ""),
        user_prefs.get("mood", ""),
        user_prefs.get("energy", 0.0),
        user_prefs.get("likes_acoustic", False),
        song.get("genre", ""),
        song.get("mood", ""),
        song.get("energy", 0.0),
        song.get("acousticness", 0.0),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, ranks by score (descending), and returns the top k as
    (song_dict, score, explanation) tuples.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
