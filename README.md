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

So far from my understanding of the real-world recommendations work, there is two different ways. One is, you like songs A,B,C,and D; then someone else likes A,B,and C as well... So I will recommend them D. It doesn't look actually into the meta data of the songs, just going off of since you liked the same I am going to recommend the same to someone else.

I am really going to score off of using genre, mood, energy, and acousticness.

My algorithmic recipe is genre match earns +2 if it equals the users favorite genre, mood match is +1, and energy similiarity is up to +2 points (sliding scale).

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
============================================================
🎵  MUSIC RECOMMENDER
============================================================
Your profile:  genre=pop  |  mood=happy  |  energy=0.8

Top 5 recommendations:

1. Sunrise City — Neon Echo
   Score: 4.96
   Reasons:
     • genre match: pop (+2.0)
     • mood match: happy (+1.0)
     • energy match (98% close) (+2.0)

2. Gym Hero — Max Pulse
   Score: 3.74
   Reasons:
     • genre match: pop (+2.0)
     • energy match (87% close) (+1.7)

3. Rooftop Lights — Indigo Parade
   Score: 2.92
   Reasons:
     • mood match: happy (+1.0)
     • energy match (96% close) (+1.9)

4. Concrete Kingdom — Verse Machine
   Score: 2.00
   Reasons:
     • energy match (100% close) (+2.0)

5. Night Drive Loop — Neon Echo
   Score: 1.90
   Reasons:
     • energy match (95% close) (+1.9)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Experiment: double the energy weight, halve the genre weight.**
I changed `GENRE_WEIGHT` from 2.0 to 1.0 and `ENERGY_WEIGHT` from 2.0 to 4.0,
then re-ran the "High-Energy Pop" profile (`genre=pop, mood=happy, energy=0.9`).

| Rank | Baseline (genre 2.0 / energy 2.0) | After (genre 1.0 / energy 4.0) |
|------|-----------------------------------|--------------------------------|
| 1    | Sunrise City — 4.84               | Sunrise City — 5.68            |
| 2    | Gym Hero — 3.94                   | Gym Hero — 4.88                |
| 3    | Rooftop Lights — 2.72             | Rooftop Lights — 4.44          |
| 4    | Storm Runner — 1.98               | Storm Runner — 3.96            |
| 5    | Pulse Reactor — 1.88              | Pulse Reactor — 3.76           |

**Result: the change made the recommendations more _different_, not more _accurate_.**
The top-5 order stayed the same, but the scores compressed — the lead of pop songs
over non-pop songs shrank from about 2 points to under 1. Genre stopped acting as a
tiebreaker and energy took over. On this small catalog the ranking is fairly robust to
reweighting, which was itself a useful thing to learn.

Other observations from running six different profiles:

- The system behaves best when a user's genre, mood, and energy all point the same way
  (e.g. "Chill Lofi" produced a clean top-5 of lofi/acoustic tracks).
- Adversarial profiles exposed weaknesses: a conflicting `mood=melancholic, energy=0.95`
  profile silently ignored the "sad" wish because no song matched that mood, and a
  `genre=kpop` profile (genre not in the catalog) fell back to mood + energy only.

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



