

**Step 3 Mapping the Logic**
*formulate a prompt to help design a math-based 'Scoring Rule'*

Context: I'm building a simple content-based music recommender in Python. Each song has a numerical energy feature normalized to 0–1. A user has a target_energy preference, also 0–1. I'm scoring each song and ranking the top results.

Problem: I need a "closeness" scoring rule for numerical features. A naive rule like score = song.energy is wrong — it just rewards higher values. What I actually want is to reward songs whose energy is near the user's target_energy, and penalize songs that are far off in either direction (too high OR too low).

Ask: Show me one or more math formulas that turn the distance between target_energy and song.energy into a score where a perfect match gives the maximum and the score decreases as they diverge. For each formula:

explain the intuition and what its curve looks like,
give the Python expression,
state the output range and how to scale it by a weight,
note the trade-offs so I can choose.
Constraints: Keep it simple and explainable (this is educational), both values are already 0–1, and it must work symmetrically for distance above and below the target.

Why this prompt works: it gives context (the data, the scale), names the anti-pattern to avoid ("just rewards higher values"), states the exact property wanted (symmetric, peaks at match), and specifies the output format (formula + intuition + code + range + trade-offs). That specificity is what separates a vague prompt from one that gets a usable answer.

*Answer*
Option A — Linear ("inverted distance")


score = weight * (1 - abs(target_energy - song.energy))
Curve: straight line. d=0 → full weight; d=1 → 0.
Range: 0 to weight. Simplest and most explainable.
Trade-off: penalizes small and large misses at the same rate — a 0.1 miss and a 0.4 miss lose proportionally the same per unit.

Scoring Rule — judges one song in isolation
Ranking Rule — decides what the list looks like