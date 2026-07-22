## Base System Implementation Plan

### Goal

Build a small Streamlit vocabulary game with five multiple-choice questions. Each question shows one word and four definitions. The player earns more points for answering correctly within 10 seconds.

Keep the first version in one file: `app.py`.

### Smallest file structure

```text
VocabuBaddie/
├── app.py
├── vocab_lists/
│   └── english_vocab_list_tester.py
└── docs/
    └── base-system-spec.md
```

No database, backend, JSON conversion, or extra game modules are needed for this step.

### Data source

Use `vocab_lists/english_vocab_list_tester.py` directly as a Python module.

Each vocabulary item already has the needed shape:

```python
{
  "word": "not",
  "frequency": 17,
  "defs": [
    "negation of a word or group of words"
  ]
}
```

For the base game:

- Use `entry["word"]` as the displayed word.
- Use `entry["defs"][0]` as the correct definition.
- Ignore `frequency` for now.
- Ignore additional items in `defs` for now.
- Build incorrect options from the first definition of other vocabulary entries.

At app startup, filter out invalid entries:

- Missing or empty `word`
- Missing, empty, or invalid `defs`
- Empty first definition

If fewer than five usable words or four distinct definitions remain, show an error and stop the game.

### Game rules

- A game contains exactly **5 questions**.
- Each question has exactly **4 definition options**.
- One option is correct; three are definitions from other words.
- A word cannot appear twice in one game.
- The player selects an option and presses **Submit Answer**.
- After submitting, show feedback and require the player to press **Next Word**.
- Scoring:
  - Correct within 10 seconds: 10 points
  - Correct after 10 seconds: 5 points
  - Incorrect: 0 points

### Core flow

1. The app loads and validates the vocabulary data.
2. The player presses **Start Game**.
3. The app resets score and game progress.
4. The app randomly selects an unused vocabulary entry.
5. The app creates four shuffled choices:
   - correct definition
   - three distinct incorrect definitions
6. The app saves the question start time.
7. The player selects an answer and presses **Submit Answer**.
8. The app calculates elapsed time, checks the answer, and updates score once.
9. The app shows correct/incorrect feedback and points earned.
10. The player presses **Next Word**.
11. After question five, the app shows the final score and a **Play Again** button.

### Session state

Use only the following Streamlit session-state values:

| Variable | Purpose |
|---|---|
| `game_started` | Whether a game is in progress. |
| `score` | Current total score. |
| `question_number` | Number of completed/current questions. |
| `used_words` | Words already selected this game. |
| `current_word` | Word currently shown to the player. |
| `correct_definition` | Correct answer for the current word. |
| `choices` | The four shuffled definition options. |
| `question_start_time` | Time when the current question was created. |
| `answered` | Prevents multiple scoring for one question. |
| `last_feedback` | Whether the last answer was correct, time taken, and points earned. |

The final screen can be shown when `question_number` reaches 5; no separate `game_finished` value is necessary.

### Build order

1. Create `app.py` and confirm it runs with Streamlit.
2. Import the existing vocabulary list from `vocab_lists/english_vocab_list_tester.py`.
3. Filter invalid entries and show a simple Streamlit error if the data cannot support the game.
4. Add a start screen with a **Start Game** button.
5. Add session-state initialization and reset logic.
6. Add question generation:
   - choose an unused word
   - use its first definition as correct
   - choose three distinct wrong definitions
   - shuffle the four choices
7. Display the word, radio-button choices, and **Submit Answer**.
8. Add answer checking, elapsed-time calculation, feedback, and scoring.
9. Add **Next Word**.
10. Add the final-score screen and **Play Again**.
11. Manually test a complete game.

### Testing checklist

- The app starts and loads the existing vocabulary module.
- Start Game begins a five-question game.
- Each question shows one word and exactly four choices.
- Each question includes its correct definition exactly once.
- Incorrect options are distinct and come from other words.
- The same word does not repeat in one game.
- Correct answers receive 10 or 5 points based on elapsed time.
- Incorrect answers receive 0 points.
- Repeated Submit clicks cannot add score twice.
- Next Word generates a new question.
- After five questions, the final score appears.
- Play Again resets score, question count, used words, and feedback.
- Invalid or insufficient vocabulary data produces a readable error.

### Risks to watch for

- Confirm the exact variable name exported by `english_vocab_list_tester.py` before importing it.
- Some entries may have empty definitions; filter them before gameplay.
- Several entries may share the same definition; ensure answer choices are unique.
- Streamlit reruns the script after each interaction, so retain all active game data in `st.session_state`.
- Save the question start time when creating the question, not after the player submits.
- A browser refresh may reset the current game. That is acceptable in the base system.

### Explicitly out of scope

- Leaderboards, databases, backend APIs, or score persistence.
- Accounts, player names, authentication, or multiplayer.
- Using `frequency` to calculate difficulty or select words.
- Categories, streaks, hints, lives, achievements, or adaptive difficulty.
- Live countdown timers or automatic question timeouts.
- Supporting multiple valid definitions from `defs`.
- External dictionary services.
- Advanced styling, animations, audio, or mobile optimization.
- Refactoring the app into multiple modules before the one-file version works.