"""A small Streamlit vocabulary quiz using the local vocabulary list."""

from __future__ import annotations

import importlib.util
import random
import time
import json
from pathlib import Path

import streamlit as st


TOTAL_QUESTIONS = 5
FAST_ANSWER_SECONDS = 10


def load_vocabulary() -> list[dict[str, str]]:
    """Load usable word/definition pairs from the local JSON data file."""
    vocab_directory = Path(__file__).resolve().parent / "vocab_lists"
    json_files = sorted(vocab_directory.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(
            f"No JSON vocabulary file found in {vocab_directory}."
        )
    if len(json_files) > 1:
        raise ValueError(
            f"Expected one JSON vocabulary file in {vocab_directory}."
        )

    with json_files[0].open("r", encoding="utf-8") as data_file:
        raw_entries = json.load(data_file)

    if not isinstance(raw_entries, list):
        raise ValueError("The vocabulary JSON file must contain a list of entries.")

    entries = []
    for entry in raw_entries:
        word = entry.get("word")
        definitions = entry.get("defs")
        if isinstance(word, str) and word.strip() and isinstance(definitions, list):
            first_definition = definitions[0] if definitions else None
            if isinstance(first_definition, str) and first_definition.strip():
                entries.append(
                    {"word": word.strip(), "definition": first_definition.strip()}
                )

    return entries


def new_question(vocabulary: list[dict[str, str]]) -> None:
    """Choose one unused word and make four unique definition choices."""
    used_words = st.session_state.used_words
    available = [entry for entry in vocabulary if entry["word"] not in used_words]
    correct_entry = random.choice(available)
    correct_definition = correct_entry["definition"]

    wrong_definitions = list(
        {
            entry["definition"]
            for entry in vocabulary
            if entry["word"] != correct_entry["word"]
            and entry["definition"] != correct_definition
        }
    )
    choices = [correct_definition, *random.sample(wrong_definitions, 3)]
    random.shuffle(choices)

    st.session_state.current_word = correct_entry["word"]
    st.session_state.correct_definition = correct_definition
    st.session_state.choices = choices
    st.session_state.question_start_time = time.time()
    st.session_state.answered = False
    st.session_state.last_feedback = None


def reset_game(vocabulary: list[dict[str, str]]) -> None:
    st.session_state.game_started = True
    st.session_state.score = 0
    st.session_state.question_number = 0
    st.session_state.used_words = []
    new_question(vocabulary)


def initialize_state() -> None:
    defaults = {
        "game_started": False,
        "score": 0,
        "question_number": 0,
        "used_words": [],
        "current_word": "",
        "correct_definition": "",
        "choices": [],
        "question_start_time": 0.0,
        "answered": False,
        "last_feedback": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


st.set_page_config(page_title="VocabuBaddie", page_icon="📚")
st.title("VocabuBaddie")
st.caption("Choose the correct definition. Answer quickly for more points.")

initialize_state()

try:
    vocabulary = load_vocabulary()
except (OSError, RuntimeError, ValueError) as error:
    st.error(f"Vocabulary data could not be loaded: {error}")
    st.stop()

unique_definitions = {entry["definition"] for entry in vocabulary}
if len(vocabulary) < TOTAL_QUESTIONS or len(unique_definitions) < 4:
    st.error("The vocabulary list needs at least 5 words and 4 unique definitions.")
    st.stop()

if not st.session_state.game_started:
    st.write(f"This game has {TOTAL_QUESTIONS} questions.")
    if st.button("Start Game", type="primary"):
        reset_game(vocabulary)
        st.rerun()
    st.stop()

if st.session_state.question_number >= TOTAL_QUESTIONS:
    st.success(f"Game complete! Your final score is {st.session_state.score} points.")
    if st.button("Play Again", type="primary"):
        reset_game(vocabulary)
        st.rerun()
    st.stop()

st.write(f"Question {st.session_state.question_number + 1} of {TOTAL_QUESTIONS}")
st.metric("Score", st.session_state.score)
st.subheader(st.session_state.current_word)

answer = st.radio(
    "Which definition is correct?",
    st.session_state.choices,
    index=None,
    disabled=st.session_state.answered,
)

if not st.session_state.answered:
    if st.button("Submit Answer", type="primary", disabled=answer is None):
        elapsed_seconds = time.time() - st.session_state.question_start_time
        is_correct = answer == st.session_state.correct_definition
        points = 10 if is_correct and elapsed_seconds <= FAST_ANSWER_SECONDS else 5 if is_correct else 0

        st.session_state.score += points
        st.session_state.answered = True
        st.session_state.last_feedback = {
            "is_correct": is_correct,
            "points": points,
            "elapsed_seconds": elapsed_seconds,
        }
        st.rerun()
else:
    feedback = st.session_state.last_feedback
    if feedback["is_correct"]:
        st.success(f"Correct! +{feedback['points']} points")
    else:
        st.error(f"Not quite. The correct definition was: {st.session_state.correct_definition}")
    st.caption(f"Answered in {feedback['elapsed_seconds']:.1f} seconds.")

    if st.button("Next Word", type="primary"):
        st.session_state.used_words.append(st.session_state.current_word)
        st.session_state.question_number += 1
        if st.session_state.question_number < TOTAL_QUESTIONS:
            new_question(vocabulary)
        st.rerun()
