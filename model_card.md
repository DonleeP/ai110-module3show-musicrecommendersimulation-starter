# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  
TheVibeFeeler
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

This recommender is a rule-based system designed to rank a small catalog of songs against a user's stated taste profile; their preferred genre, mood, target energy level, and whether they favor acoustic music.

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Think of it like a points contest between songs. You tell the app your favorite genre, your mood, and how much energy you want. Each song earns points: a good chunk for matching your genre, a smaller bonus for matching your mood, and points for energy based on how close it is to what you asked for — near-perfect earns almost full points, way-off earns almost none. There's also a small bonus for acoustic songs if you like those. The app adds up each song's points, lines them up highest to lowest, and hands you the top few with a note on where their points came from. My main change from the starter was the scoring itself: the starter just returned the first few songs without judging them, so I made genre count most, mood less, and energy a sliding "how close" score.

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

I used the original 10 songs and had Claude add more diverse songs and ranges that werent already included.

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

It works great when your genre, mood, and energy all point the same direction — like "Chill Lofi," where the top picks were all exactly the kind of calm, acoustic tracks you'd want. It nails the obvious matches: ask for pop/happy/high-energy and the pop, happy, upbeat song lands at #1 every time. And it always tells you why a song showed up, so the results never feel like a black box. It also doesn't fall apart on weird inputs — leave out your genre or pick one that isn't in the catalog and it still gives you a sensible list instead of crashing.



Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly.

**1. Genre echo chamber (filter bubble).** A genre match is the single biggest source
of points and is exact-match only. The system never gives a real chance to anything
outside the user's stated genre, so the user only ever sees more of what they already
asked for. Related labels are also treated as strangers — "indie pop" never satisfies a
"pop" fan, even though a human would consider them close.

**2. The energy gap quietly favors mid-energy songs.** Because the energy score scales
with `1 − |song − target|`, a song at energy 0.5 is within 0.5 of *every* possible target,
while a 0.98 song is far from any low-energy listener. Extreme-energy songs (ambient at
0.28, metal at 0.98) are structurally penalized and can only score well for a narrow slice
of users. This is a subtle bias built into how the "gap" is calculated.

**3. Mood is exact-match and fails silently.** "melancholic," "sad," and "moody" are
treated as completely unrelated. A near-miss earns zero points, and — more importantly —
the user gets no signal that their preference was dropped. A conflicting profile
(`mood=melancholic, energy=0.95`) simply returned loud pop songs as if the mood request
had never been made.

**4. Features it does not consider.** The model ignores tempo, valence, danceability,
artist, release year, and lyrics/language entirely, even though those columns exist in the
data. Two songs can look identical to the scorer while feeling very different to a person.

**5. Catalog bias (data, not algorithm).** With only 18 songs — and just one rock, one
metal, and one classical track — thin genres can never fill a top-5. The ranking then
leans on energy and produces odd cross-genre lists (e.g. a "Deep Intense Rock" user gets
pop and edm songs after the single rock track runs out).

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected.

**Profiles tested.** I stress-tested the recommender against six profiles: three
"normal" tastes (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial
edge cases (a conflicting sad-but-hyper profile, a genre not in the catalog, and a
profile with no genre key at all).

**What I looked for.** Whether the top results made intuitive sense, whether the reasons
shown for each song added up to its score, and whether unusual inputs broke the system or
produced misleading results.

**What surprised me.**
- The adversarial profiles revealed that unmatched preferences (a missing mood or genre)
  are dropped *silently* — the user never learns their wish was ignored.
- The genre-not-in-catalog and no-genre-key profiles did **not** crash; the scorer's
  `.get()` calls let it degrade gracefully to whatever preferences were provided.
- In the weight-shift experiment (double energy, halve genre), the rankings barely moved —
  only the scores compressed. The system was more robust to reweighting than I expected,
  largely because the catalog is so small.

**Automated tests.** The two starter tests in `tests/test_recommender.py` pass, confirming
that `recommend()` returns songs sorted by score and that `explain_recommendation()`
returns a non-empty explanation string.

---

## 8. Future Work  

Ideas for how you would improve the model next.  
Fix silent failures: when no song matches your mood or genre, say so instead of quietly dropping it.
Treat similar labels as related: let "indie pop" count (partially) for a "pop" fan, and group moods like "sad/melancholic/moody" so near-misses still earn something.
Use more of the data: the songs already have tempo, valence, and danceability columns the scorer ignores — adding them would make matches richer.
Add variety to the top-5: nudge the results so you don't get five near-identical songs, breaking the genre "echo chamber."
Grow the catalog: 18 songs is too few for thin genres like rock or classical to ever fill a list — more data would fix a lot of the odd cross-genre results.


Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

I learned how deep the code gets for music recommendations/recommendations in general. It is pretty complex but almost not at the same time. I am sure bigger music companies probably have some REALLY complex stuff haha.

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  



Personal Reflection:

My biggest learning for sure is the scoring aspect of the project and how complex it is and how there is many different ways you could score. 

AI tools were really helpful in the sense of making songs diverse and adding onto the data file. As well as running quick tests to make sure I didn't break anything as time went on. Sometimes I would have to hold the AI back from trying to read into too much and jumping ahead on steps.

If I was to extend the project I would definitely add stuff like fixing the silent failures, Using way more data, and add more variety to the rankings.
