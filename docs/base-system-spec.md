## Project goal

Build a small Streamlit vocabulary game where a player sees an uncommon English word, chooses the correct definition from four options, and earns a score influenced by how quickly they answer.

## Minimum features

- Start/restart game button.
- Display one word at a time.
- Show exactly four definition choices.
- Let the player select one answer and submit it.
- Tell the player whether the answer was correct.
- Track score during the game.
- Apply a simple time-based score rule.
- Move to the next word.
- End the game after a fixed small number of questions, such as 5.
- Show final score and allow restart.
- Load words and definitions from a local JSON file.

## Simple gameplay flow

1. Player opens the app and presses **Start Game**.
2. The app selects a word that has not yet been used this game.
3. The app records the question start time.
4. The player sees the word and four shuffled definitions.
5. The player selects an answer and presses **Submit**.
6. The app calculates elapsed time and checks the answer.
7. The app shows correct/incorrect feedback and adds points if correct.
8. The player presses **Next Word**.
9. Steps 2–8 repeat until the fixed number of questions is reached.
10. The app shows the final score and a **Play Again** button.

## JSON data needed

Each word needs:

- `word`: the vocabulary word to show.
- `definition`: its correct definition.
- `difficulty` *(optional for now)*: a simple label such as `"low_frequency"`.

Example:

```json
[
  {
    "word": "algebra",
    "frequency": 8151,
    "defs": [
      "the mathematics of generalized arithmetical operations"
    ]
  }
]
```

The app can create wrong options by using definitions belonging to other words in the same file.

## Simple scoring rule

Keep it easy to verify:

- Correct answer within 5 seconds: 5 points.
- Correct answer after 3 seconds: 3 points.
- Incorrect answer: 0 points.

Use the time from when the question is displayed until **Submit** is pressed.

## Main edge cases

- JSON file is missing, empty, or invalid.
- There are too few words to create four unique answer options.
- A definition appears more than once, causing duplicate options.
- The player submits without selecting an answer.
- The player clicks Submit more than once for the same question.
- The player refreshes the page; Streamlit session state may reset.
- The game requests more questions than available words.
- The same word appears twice in one game.
- Timer/session state is lost or incorrectly reset when the page reruns.

## Small, realistic first scope

Aim for:

- One local JSON file with at least 15–20 word entries.
- A 5-question game.
- Four choices per question.
- One simple score rule based on a 10-second threshold.
- In-memory session state only.
- Basic text-based Streamlit interface; no custom styling required.

## Explicitly out of scope

- Leaderboards or backend/database storage.
- User accounts, login, or player names.
- Multiplayer.
- Saving past games or high scores.
- Difficulty levels, categories, streak bonuses, hints, or lives.
- Adaptive question selection.
- Audio, animations, advanced visual design, or mobile optimization.
- Editing words in the app.
- External dictionary APIs or generated definitions.
- Anti-cheating measures or precise real-time countdown behavior.