## 1. Extension goal

Add a simple SQLite-backed high-score system so players can enter a username after a game, save their final score, and view the top 10 scores.

## 2. Minimum features

- Create the SQLite database automatically if it does not exist.
- Create a scores table automatically if it does not exist.
- Show a username input after the game ends.
- Save the player’s final score with their username.
- Prevent the same completed game from being saved twice.
- Show a leaderboard with the top 10 scores.
- Display leaderboard rank, username, score, and saved date/time.
- Show a clear message if saving or loading scores fails.

## 3. User flow

1. Player completes the final question of a game.
2. The app shows the final score.
3. The app asks the player to enter a username.
4. The player presses **Save Score**.
5. The app validates the username.
6. The app saves the username, final score, and timestamp to SQLite.
7. The app confirms that the score was saved.
8. The app displays the top-10 leaderboard.
9. The player can choose **Play Again** to start a new game.

If the player does not want to save, they can still view the leaderboard and start another game.

## 4. Data stored for each score

Each saved score should contain:

| Field | Purpose |
|---|---|
| `id` | Unique database record identifier. |
| `username` | Name entered by the player. |
| `score` | Final score for that completed game. |
| `created_at` | Date and time when the score was saved. |

A simple table shape is:

```text
scores
- id
- username
- score
- created_at
```

Do not store passwords, accounts, detailed answer history, browser information, or personal data.

## 5. Validation and error handling

- Username is required before saving.
- Trim spaces before validation.
- Limit usernames to a small maximum length, such as 20 characters.
- Reject blank usernames after trimming.
- Allow simple letters, numbers, spaces, underscores, and hyphens.
- Confirm that the current game has actually ended before allowing a score save.
- Store score as a non-negative integer.
- Disable or hide Save Score after a successful save.
- If database setup fails, show a readable error instead of crashing.
- If inserting a score fails, show a readable error and allow the player to try again.
- If leaderboard loading fails, show a readable error.

## 6. Main edge cases

- The database file does not exist on first launch.
- The scores table does not exist yet.
- The player tries to save without a username.
- The username contains only whitespace.
- The username is too long or contains unsupported characters.
- The player clicks Save Score more than once.
- The player refreshes after completing a game but before saving.
- The player starts a new game before saving the previous score.
- Several players have the same score.
- Fewer than 10 scores exist.
- Database file permissions prevent writing.
- The database file is missing, corrupted, or unavailable.
- The app is opened by multiple users at once; SQLite may temporarily lock during simultaneous writes.

For tied scores, use most recently saved first or oldest saved first, but choose one rule and keep it consistent. For a first version, sorting by highest score, then earliest saved score, is simple and fair.

## 7. Out of scope

- User accounts, passwords, login, or authentication.
- Editing or deleting saved scores.
- Per-user score history.
- Preventing users from choosing the same username.
- Cheating prevention or score verification beyond checking that the game ended.
- Cloud database hosting or shared production deployment.
- Multiplayer or real-time leaderboard updates.
- Pagination, searching, filtering, or leaderboard categories.
- Saving individual answers, timing details, or game history.
- Admin tools.
- Database migrations beyond creating the initial table if missing.