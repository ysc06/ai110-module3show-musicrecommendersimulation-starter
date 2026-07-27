# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

### Song features

Each `Song` stores the following fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | int | Unique identifier |
| `title` | str | Song title |
| `artist` | str | Performer |
| `genre` | str | Category label (e.g. indie, pop) |
| `mood` | str | Mood label (e.g. chill, happy) |
| `energy` | float | How energetic, on a scale |
| `tempo_bpm` | float | Speed in beats per minute |
| `valence` | float | Musical positivity / happiness |
| `danceability` | float | How suitable for dancing |
| `acousticness` | float | How acoustic vs. electronic |

My scoring rule pays attention to four of these — `genre`, `mood`, `energy`, and `acousticness`. The rest (`tempo_bpm`, `valence`, `danceability`) exist in the data but aren't used in scoring yet.

### User profile features

A `UserProfile` stores what a listener tends to like:

| Field | Type | Meaning |
|---|---|---|
| `favorite_genre` | str | Preferred genre (e.g. `indie`) |
| `favorite_mood` | str | Preferred mood (e.g. `chill`) |
| `target_energy` | float | Desired energy level |
| `likes_acoustic` | bool | Whether they prefer acoustic songs |

**Scoring.** For each song, the `Recommender` compares the song's features against the user's profile and adds up a score:

- Matching `genre` and `mood` earn points.
- `energy` is compared to `target_energy` — the closer the song is to the target, the higher the score (a smaller distance means a better match).
- If the user `likes_acoustic`, songs with higher `acousticness` are rewarded.

**Choosing recommendations.** After every song is scored, I sort them from highest to lowest and return the top 5.

**What my version prioritizes.** My design leans on matching *taste labels* first: a song that shares the user's `genre` and `mood` gets the biggest boost, because those are the strongest signals of whether someone will like it. `energy` closeness matters next as a tie-breaker, and `acousticness` is a smaller nudge that only counts when the user says they like acoustic music. In short, I prioritize **the right genre and mood over a perfect energy match** — I'd rather recommend a slightly-too-energetic indie/chill song than a perfectly-energetic song from a genre the user doesn't like.

**How this mirrors real-world recommenders.** Real systems like Spotify or YouTube work the same way at heart: they turn songs and users into features (numbers and labels), score how well each item matches a person's taste, and rank the results. The big differences are scale and where the profile comes from — instead of a handful of hand-set preferences, real recommenders learn a user's taste from millions of listening events and often compare users to each other ("people like you also liked..."). My simulation is a tiny, hand-built version of that same score-and-rank idea.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Below is the actual terminal output from `python -m src.main` for the default
**"The Focused Studier"** profile (`genre=lofi`, `mood=focused`, `energy=0.4`,
`likes_acoustic=True`):

```
Loading songs from data/songs.csv...
Loaded songs: 18

Top recommendations:

Focus Flow - Score: 100.00
Because: matches your favorite genre (lofi); matches your mood (focused); energy 0.40 is close to your target 0.40; has the acoustic texture you enjoy

Midnight Coding - Score: 87.50
Because: matches your favorite genre (lofi); has a related mood (chill ~ focused); energy 0.42 is close to your target 0.40; has the acoustic texture you enjoy

Library Rain - Score: 86.75
Because: matches your favorite genre (lofi); has a related mood (chill ~ focused); energy 0.35 is close to your target 0.40; has the acoustic texture you enjoy

Coffee Shop Stories - Score: 52.25
Because: has a related mood (relaxed ~ focused); energy 0.37 is close to your target 0.40; has the acoustic texture you enjoy

Spacewalk Thoughts - Score: 50.00
Because: has a related mood (chill ~ focused); energy 0.28 is close to your target 0.40; has the acoustic texture you enjoy
```

The top result, *Focus Flow*, scores a perfect 100 because it matches the
profile on every signal (lofi genre, focused mood, exact energy, acoustic
texture). The next results are other lofi/acoustic tracks whose moods are
*adjacent* to "focused," which is exactly what a studier would want next.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



