import streamlit as st
import google.generativeai as genai
import random
import pandas as pd
from config import api_key
from streamlit_sortables import sort_items

# Configure Gemini API
GEMINI_API_KEY = api_key
genai.configure(api_key=GEMINI_API_KEY)

# Load dataset
DATASET_PATH = r"C:\Users\Vigasini\Downloads\sentence_dataset_50k.csv"
df = pd.read_csv(DATASET_PATH)
sentence_list = df["sentence"].tolist()

# Initialize session state
if "level" not in st.session_state:
    st.session_state.level = 1  # Start at Level 1 (3-word sentences)
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0  # Track consecutive correct answers
if "previous_sentences" not in st.session_state:
    st.session_state.previous_sentences = set()  # Avoid duplicate sentences
if "last_sentence" not in st.session_state:
    st.session_state.last_sentence = ""  # Track last sentence to prevent repetition
if "current_sentence" not in st.session_state or not st.session_state.current_sentence:
    st.session_state.current_sentence = ""
if "jumbled_words" not in st.session_state:
    st.session_state.jumbled_words = []
if "first_puzzle_solved" not in st.session_state:
    st.session_state.first_puzzle_solved = False  # Track if the first sentence has been used

# Function to generate a new sentence based on level
def get_sentence():
    word_count = 3 + (st.session_state.level - 1)  # Start with 3 words, increase with levels

    # Try getting a sentence from the dataset
    filtered_sentences = [s for s in sentence_list if len(s.split()) == word_count]
    filtered_sentences = [s for s in filtered_sentences if s != st.session_state.last_sentence]

    if filtered_sentences:
        sentence = random.choice(filtered_sentences)
        st.session_state.last_sentence = sentence  # Store last sentence to prevent repetition
        return sentence

    # If no matching sentence is found in the dataset, generate one using Gemini
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    prompt = f"Generate a simple, grammatically correct English sentence with exactly {word_count} words."
    response = model.generate_content(prompt)
    
    if hasattr(response, "text") and response.text.strip():
        generated_sentence = response.text.strip()
        st.session_state.last_sentence = generated_sentence
        return generated_sentence

    # Fallback sentence
    return "I love cats" if word_count == 3 else "I love my cat very much"

# Function to reset the game state for a new sentence
def reset_sentence():
    new_sentence = get_sentence()

    # Ensure first puzzle gets replaced after solving once
    while new_sentence == st.session_state.current_sentence:
        new_sentence = get_sentence()

    st.session_state.current_sentence = new_sentence
    st.session_state.jumbled_words = new_sentence.split()
    random.shuffle(st.session_state.jumbled_words)

# Ensure a sentence is loaded at the start or when level changes
if "prev_level" not in st.session_state or st.session_state.level != st.session_state.prev_level:
    reset_sentence()
    st.session_state.prev_level = st.session_state.level  # Track level changes

correct_sentence = st.session_state.current_sentence.strip()

# Streamlit UI
st.title("Sentence Formation Game")
st.write(f"**Level {st.session_state.level}:** Rearrange the words to form a correct sentence.")

st.write("### Jumbled Words:")
st.write("Drag and drop to reorder:")

# Ensure words exist before rendering UI
if st.session_state.jumbled_words:
    sorted_words = sort_items(st.session_state.jumbled_words, direction="horizontal", key=f"sortable_words_{st.session_state.level}_{st.session_state.correct_answers}")

    if st.button("Check Sentence"):
        ordered_sentence = " ".join(sorted_words).strip()  # Trim spaces to avoid false negatives
        if ordered_sentence == correct_sentence:
            st.success("Correct! Moving to the next level...")
            st.session_state.correct_answers += 1

            # Increase level after 2 correct answers
            if st.session_state.correct_answers >= 2:
                st.session_state.level += 1
                st.session_state.correct_answers = 0  # Reset correct answer count

            reset_sentence()  # Ensure new sentence is set before rerun
            st.rerun()  # Correct function for rerunning in latest Streamlit versions
        else:
            st.error("Incorrect! Try again.")
else:
    st.error("No words available. Please refresh the page.")
