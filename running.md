# Running the Project

## Prerequisites

* Python 3.11 or newer
* Git (to clone the repository)

## Setup

Clone the repository:

```bash
git clone https://github.com/jaebender/VocabuBaddie
cd VocabuBaddie
```

Create and activate a virtual environment.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Your browser should automatically open the application. If it does not, Streamlit will display a local URL (typically http://localhost:8501).

## Playing the Game

1. Click **Start Game**.
2. Select a difficulty level.
3. Read the displayed word.
4. Choose the correct definition from the four multiple-choice options.
5. Continue until the game ends.
6. Enter a username to save your score.
7. View the Top 10 leaderboard.
8. Click **Play Again** to begin a new game.

## Notes

* The vocabulary is loaded from the JSON file included in the repository.
* The SQLite database (`scores.db`) is created automatically the first time a score is saved.
* The database file is intentionally excluded from version control using `.gitignore`.
