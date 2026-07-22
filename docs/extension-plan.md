## Extension implementation plan

### Goal

Add persistent high scores to the existing Streamlit vocabulary game. After completing a game, a player enters a username, saves their final score to SQLite, and sees the top 10 leaderboard.

### Smallest file structure

```text
VocabuBaddie/
├── app.py
├── scores.db                  # created automatically; do not commit
├── vocab_lists/
│   └── ...
└── docs/
    └── extension-spec.md
```

Keep the extension inside the existing `app.py`. No new Python modules are required.

Add `scores.db` to `.gitignore` if the project uses Git.

### Database design

Use one local SQLite file located beside `app.py`, based on the app file’s path rather than the current working directory.

Use one table:

```text
scores
- id: unique integer record ID
- username: player-entered name
- score: final game score
- created_at: saved date/time
```

The table should be created automatically when needed if the database or table does not yet exist.

Leaderboard order:

1. Highest score first.
2. For equal scores, earliest saved score first.
3. Show no more than 10 rows.

### Minimal helper responsibilities

Add three small database helpers near the top of `app.py`:

1. **Initialize database**
   - Open the SQLite file.
   - Create the `scores` table if it does not exist.
   - Close the connection.

2. **Save score**
   - Insert username, score, and timestamp.
   - Use a parameterized SQL insert.
   - Close the connection.
   - Return success or allow the app to display an error.

3. **Get top scores**
   - Query the top 10 scores in leaderboard order.
   - Return the rows.
   - Close the connection.

Use only standard Python libraries: `sqlite3`, `pathlib`, and `datetime`, plus Streamlit.

### Changes to the existing game flow

Keep the base game unchanged until the final-score screen.

At the end of a completed game:

1. Display the final score.
2. If this game has not been saved:
   - Display a username text input.
   - Display a **Save Score** button.
3. When Save Score is pressed:
   - Trim the username.
   - Require a non-empty username.
   - Limit it to 20 characters.
   - Confirm the game is complete.
   - Initialize the database if needed.
   - Save the final score.
   - Mark the game as saved.
   - Show a success message.
4. Read and display the top 10 leaderboard.
5. Keep the existing **Play Again** button.

If the player does not save a score, still show the leaderboard and allow Play Again.

### Session state

Add one state variable:

| Variable | Purpose |
|---|---|
| `score_saved` | Prevents the final score from being inserted more than once for the current game. |

Set `score_saved` to `False` when a new game starts or restarts.

Set it to `True` only after SQLite successfully saves the score.

Do not store the SQLite connection or leaderboard data in session state.

### Build order

1. Add standard-library imports for SQLite, paths, and timestamps.
2. Define a fixed `scores.db` path beside `app.py`.
3. Add database initialization that creates the scores table if missing.
4. Add score-save helper using parameterized SQL.
5. Add top-10 query helper.
6. Add `score_saved` to session-state initialization.
7. Reset `score_saved` in the existing new-game/reset function.
8. Update only the final-score screen:
   - username input
   - Save Score behavior
   - leaderboard display
   - existing Play Again button
9. Add `scores.db` to `.gitignore`.

### Testing checklist

- Launching with no database creates `scores.db` automatically when the leaderboard or save feature is used.
- The database table is created automatically.
- A completed game can save one valid username and final score.
- Blank or whitespace-only usernames cannot be saved.
- Usernames longer than 20 characters cannot be saved.
- Save Score cannot insert the same game twice.
- Play Again resets `score_saved`.
- Scores remain after stopping and restarting Streamlit.
- The leaderboard shows at most 10 rows.
- Scores appear from highest to lowest.
- Ties follow the chosen timestamp order.
- An empty leaderboard shows a friendly message.
- Database failures show a readable Streamlit error.

### Risks and boundaries

- Use a database path based on `app.py`, not the command-line working directory.
- Keep SQLite connections short-lived: open, perform one action, close.
- Use ISO-style timestamps so text sorting remains reliable.
- Streamlit reruns after button presses; session state is required to block duplicate saves.
- If SQLite is temporarily locked or inaccessible, show an error and let the player retry.

### Out of scope

- New backend services, APIs, cloud databases, or ORMs.
- Accounts, passwords, authentication, or unique usernames.
- Editing/deleting scores or player score history.
- Multiplayer, real-time updates, search, filters, or leaderboard categories.
- Detailed game records, answer history, analytics, or anti-cheating systems.