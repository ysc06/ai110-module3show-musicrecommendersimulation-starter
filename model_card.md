# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**TuneMatch 1.0**

A small "vibe matcher" that ranks songs by how well they fit a listener's stated taste.

---

## 2. Intended Use

**Goal / Task.** TuneMatch tries to guess which songs a person will enjoy. It does not
predict a rating or a play count. Instead it scores every song in a small catalog against a
short taste profile, then suggests the top few.

- **What it recommends:** the top 5 songs that best match one user's genre, mood, energy,
  and acoustic preferences.
- **Assumptions about the user:** the user can describe their taste with a few simple labels
  (a favorite genre, a favorite mood, a target energy level, and whether they like acoustic
  music). It assumes those few labels are enough to describe what they want right now.
- **Who it is for:** this is a **classroom exploration**, not a real product. It is meant to
  show how a score-and-rank recommender works, not to serve real listeners.

**Non-intended use.** TuneMatch should **not** be used to make real product decisions, to
judge an artist's quality, or to claim anything about a person's identity or personality from
their music taste. It is too small and too simple for any of that.

---

## 3. How the Model Works

Imagine a judge who gives each song a score out of about 100, then lines the songs up from
best to worst.

- The judge looks at **four things** about each song: its **genre**, its **mood**, its
  **energy** level, and how **acoustic** it sounds.
- It compares those to what the user said they like.
- **Genre** matters most. A matching genre earns the biggest chunk of points.
- **Mood** is next. An exact mood match earns full points. A *related* mood (for example,
  "chill" when you asked for "focused") earns partial points, because close moods still feel
  right.
- **Energy** is scored by closeness. The nearer a song's energy is to the user's target, the
  more points it gets. A perfect match gets the most; a big gap gets almost nothing.
- **Acoustic** is a smaller nudge. If the user likes acoustic music and the song is acoustic,
  it gains a few points. If they wanted acoustic and the song isn't, it loses a few. If they
  dislike acoustic but the song is very acoustic, it loses the most.

Every song also gets a short list of **reasons** ("matches your favorite genre," "energy is
close to your target") so the user can see *why* it was picked.

**Changes from the starter logic.** The starter just added flat points for exact matches. I
made three upgrades: (1) I weighted the features so genre outranks mood, and mood outranks
energy; (2) I added a "related mood" idea so near-miss moods still earn partial credit; and
(3) I made the acoustic signal work both ways — it can reward *or* penalize a song.

---

## 4. Data

- **Size:** 18 songs in `data/songs.csv`.
- **Features per song:** id, title, artist, genre, mood, energy, tempo, valence,
  danceability, and acousticness. The model only uses **genre, mood, energy, and
  acousticness** for scoring; the rest are stored but unused so far.
- **Variety:** the catalog covers many genres (pop, lofi, rock, jazz, ambient, hip hop,
  classical, electronic, country, reggae, metal, r&b, folk, indie pop, synthwave) and many
  moods (happy, chill, intense, focused, relaxed, moody, energetic, nostalgic, romantic,
  and more). Each genre usually appears only once or twice.
- **Changes I made:** I added a `danceability` column so the data lines up with the fields
  the code expects.
- **What's missing:** the dataset is tiny and hand-made. It has no lyrics, no language, no
  release year, no popularity, and no real listening history. Most genres have only one
  example, so there is very little to choose from within any single taste.

---

## 5. Strengths

- **Clear favorites:** for a user whose taste matches a well-covered corner of the catalog
  (like the default "Focused Studier" — lofi, focused, low energy, acoustic), the top pick is
  an obvious bullseye. *Focus Flow* scores a perfect 100 because it matches on every signal.
- **Sensible runners-up:** the "related mood" rule means the next picks are other lofi tracks
  whose moods are close to "focused" (chill), which is exactly what you'd want to hear next.
- **Explainable:** every recommendation comes with plain-English reasons, so the ranking
  never feels like a black box.
- **Matched my intuition:** when I set an energetic pop profile, upbeat pop songs rose to the
  top, which is what I expected.

---

## 6. Limitations and Bias

- **Features it ignores:** tempo, valence, and danceability are in the data but not scored,
  so two songs that differ only in tempo look identical to the model.
- **Genre is king:** because genre carries the most weight, a great mood-and-energy match in
  the "wrong" genre can never beat a same-genre song. This can trap a user in one genre.
- **Underrepresented tastes:** genres with only one song (metal, classical, reggae, etc.)
  give the user almost no real choice — the "top 5" for a metal fan is mostly filler.
- **Exact-label bias:** the model rewards songs whose genre label matches *exactly*. It
  doesn't know "indie pop" and "pop" are cousins, so it treats them as unrelated.
- **No diversity control:** the top results often cluster in one genre and mood, so the list
  can feel repetitive instead of offering variety.

---

## 7. Evaluation

- **Profiles I tested:**
  - *The Focused Studier* (lofi / focused / low energy / acoustic) — the default.
  - A pop / happy / high-energy profile.
  - A profile whose genre only appears once in the catalog.
- **What I looked for:** did the #1 pick make obvious sense? Did the reasons match the score?
  Did near-miss moods still show up? Did anything absurd rank highly?
- **Comparisons I ran:** I mentally raised and lowered the genre weight to see how much it
  dominated the ranking, and I checked that turning `likes_acoustic` on and off changed which
  songs won.
- **Automated checks:** the two tests in `tests/test_recommender.py` pass, confirming the
  scoring and ranking behave as expected on a small fixed example.
- **What surprised me:** even with only four features and simple arithmetic, the ranked list
  felt genuinely "curated." A perfect-match song jumping to exactly 100 while related songs
  filled in behind it looked a lot like a real app's playlist.

---

## 8. Future Work

- **Use more features:** fold in tempo, valence, and danceability so songs stop looking
  identical when only those differ.
- **Softer genre matching:** treat related genres (pop / indie pop) as partial matches, the
  same way moods already work.
- **Add diversity:** make sure the top 5 aren't all the same genre, so the list feels more
  like a varied playlist.
- **Richer profiles:** let a user list *several* liked genres or moods instead of just one,
  and learn preferences from past picks instead of asking for them up front.

---

## 9. Personal Reflection

My biggest learning moment was realizing that a "recommendation" is really just **scoring and
sorting**. Once I saw that the recommender was a loop that scores every song and then sorts
the list, the mystery disappeared — recommenders aren't magic, they're a judge with a
rulebook and a sort function.

AI tools helped me most with the *shape* of the code: turning my scoring recipe into clean
Python, explaining the difference between `.sort()` and `sorted()`, and formatting the
terminal output. But I still had to double-check them. The clearest example was an import bug
— the code looked fine but `python -m src.main` crashed, and I had to reason about how Python
packages actually resolve imports rather than trusting that it "should work." AI is great at
drafting; I'm responsible for verifying it runs and does what I meant.

What surprised me most is how *convincing* a simple algorithm can feel. There's no machine
learning here and only four features, yet watching a perfect-match song shoot to a score of
100 while related songs settled in behind it felt exactly like opening a music app and seeing
a playlist made "just for me." It made me realize how much of that real-app feeling comes
from good explanations and sensible ranking, not necessarily from complex math.

If I extended this project, I'd add the unused features (tempo, valence, danceability), make
genre matching softer so related styles count, and add a diversity rule so the top picks
aren't all the same vibe. I'd also like to learn a profile from listening history instead of
asking the user to fill one in, since that's the step that would make it feel like a real
recommender.
