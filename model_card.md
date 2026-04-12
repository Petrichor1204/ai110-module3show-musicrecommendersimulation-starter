# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0** 

SoundProfile
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
Generates song recommendations from a small catalog based on a user's stated mood, preferred genre, and energy level. Does not learn from listening history or past behavior.

- What assumptions does it make about the user  
Assumes user knows what they want and can express it through a few simple attributes.

- Is this for real users or classroom exploration  

Classroom exploration
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.) 

genre, mood numeric energy level (0-1), valence score

- What user preferences are considered  

mood match, genre match, energy proximity (how close the song's energy is to the user's), valence proximity (how positive or bright sounding a song is)

- How does the model turn those into a score  

Mood match is worth up to 30 points, Genre match is 25 points, Energy proximity 20 points, valence proximity, 15 points. 
These numbers are summed up to produce the final score. The score with the highest total wins top recommendation.

- What changes did you make from the starter logic  

Built scoring. Songs that match the user's mood get +30 points, genre gets +25. Energy and valence use a proximity formula. All songs get scored, sorted highest to lowest, and the top 5 are returned with an explanation of why each was picked.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  

18 songs

- What genres or moods are represented  
pop, lofi, rock, hip-hop, indie pop, ambient, sythwave, jazz, r&b, country, electronic, metal, classical, soul, reggae.

- Did you add or remove data 
Yes, i added more songs.

- Are there parts of musical taste missing in the dataset  

The catalog skews toward English-language Western genres — k-pop, Latin, Afrobeats, and other globally popular styles are absent. Also, with only 18 songs, many user profiles will never get a full mood+genre match, which means the continuous signals (energy, valence) end up carrying more weight than intended.
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
A pop, or happy, or high-energy user
Ambient, or chill profile

- Any patterns you think your scoring captures correctly  

Energy and valence proximity scores. 
hey correctly separated songs within the same mood/genre cluster by how well they matched the user's intensity preference. 

- Cases where the recommendations matched your intuition  

Even when no perfect match exists, the system returns something rather than failing.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The formula (1 - abs(gap)) * 20 is always ≥ 0. A song with a maximum energy mismatch still earns 0 points from this factor — it never goes negative. This means no song is ever down-ranked for energy mismatch, only up-ranked for proximity. For low-energy users (e.g., target energy = 0.2), a high-energy song like Throne of Static (energy = 0.97) still earns (1 - 0.77) * 20 = 4.6 energy points, which may push it into recommendations despite being a terrible fit.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
Tested 9 profiles including pop fan, chill indie listener, hip-hop head, high energy sad person, etc.


- What you looked for in the recommendations  

For the Pop Fan — did the top song match on mood and genre, or just one?
For the Sad Person — did sad songs actually rank above angry ones?
For the Impossible Combo — did any song come close to the intent at all?

- What surprised you  

why "Gym Hero" keeps appearing for unrelated profiles

- Any simple tests or comparisons you ran  

Pop Fan vs. Chill Indie Listener — Pop Fan got a near-perfect score because pop is well-represented; Indie Listener silently got lofi instead, because "indie" doesn't exist in the catalog
Hip-Hop Head vs. High-Energy Sad Person — both wanted high energy, but the Sad Person's top result was an angry metal song, not a sad one — genre+energy outscored the mood match
Unknown Genre/Mood vs. Case Sensitivity Trap — both ended up ranking by energy proximity only; one by design, one by a capital letter typo — system couldn't tell the difference
Out-of-Range Energy vs. All-Neutral — OOR silently neutered the energy signal; All-Neutral worked cleanly — shows valid inputs produce valid outputs
Impossible Combo (with/without mood) — disabling mood made the angry song disappear entirely; genre breadth completely took over
No need for numeric metrics unless you created some.

In general, the scoring rewards partial matches across many signals over a single perfect match, which is the opposite of what a user expects
---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
Replacing the all-or-nothing categorical matching with partial credit. 
Add tempo (BPM) as a scoreable preference.

- Better ways to explain recommendations  
Instead of listing every signal that contributed points, the explanation should lead with the most meaningful reason. 

- Improving diversity among the top results  
Add a penalty for consecutive songs with the same mood or genre. Right now the top 5 can easily be five lofi/chill songs. 

- Handling more complex user tastes  

Allow users to rank their own preferences — "genre matters more to me than mood." 
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  

A recommender system always returns an answer — which makes it easy to miss when the answer is wrong. The scoring logic doesn't know the difference between a great match and a confident mistake.

- Something unexpected or interesting you discovered 

Disabling the mood check changed the rankings dramatically for some profiles and barely at all for others. 

- How this changed the way you think about music recommendation apps  
When a real app recommends something that feels close but wrong, it's probably not a fluke. Some signal is being overruled by another one you didn't know was being weighted. 


## How AI helped 
I used AI in implementing functions and evaluating my ideas. AI helped most with the adversarial profile design — it systematically identified edge cases in the scoring logic (out-of-range inputs, case sensitivity, missing keys) that I likely would have missed testing manually.

I had to double-check when it implemented extra stuff beyond what I asked and when it missed some scoring logic. 