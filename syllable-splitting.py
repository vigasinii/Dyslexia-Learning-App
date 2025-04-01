import random
import pandas as pd
import numpy as np
import time
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class MLSyllableSplittingModule:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)
        self.df['word'] = self.df['word'].astype(str).str.strip().str.lower()
        self.df['syllables'] = self.df['syllables'].astype(str).str.strip().str.lower()
        self.df['syllable_count'] = self.df['syllables'].apply(lambda x: len(x.split('-')))

        self.word_pool = {
            1: self.df[self.df['syllable_count'] == 1][['word', 'syllables']].values.tolist(),
            2: self.df[self.df['syllable_count'] == 2][['word', 'syllables']].values.tolist(),
            3: self.df[self.df['syllable_count'] >= 3][['word', 'syllables']].values.tolist()
        }

        self.performance_data = []
        self.difficulty_level = 1
        self.consecutive_correct = 0
        self.model = RandomForestClassifier(n_estimators=100)
        self.trained = False

    def collect_data(self, difficulty, correct, response_time):
        self.performance_data.append([difficulty, correct, response_time])
        if len(self.performance_data) >= 20:
            self.train_model()

    def train_model(self):
        df = pd.DataFrame(self.performance_data, columns=['difficulty', 'correct', 'response_time'])

        if len(df) < 2:
            return

        df['next_difficulty'] = df['difficulty'].shift(-1).fillna(df['difficulty'])
        X = df[['difficulty', 'correct', 'response_time']]
        y = df['next_difficulty']

        if len(X) < 2:
            return

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if len(y_test) == 0:
            return

        self.model.fit(X_train, y_train)
        self.trained = True

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        st.write(f"📊 Model Accuracy: {accuracy:.2f}")

    def predict_difficulty(self, correct, response_time):
        if self.trained:
            prediction = self.model.predict([[self.difficulty_level, correct, response_time]])
            self.difficulty_level = int(prediction[0])
        else:
            if correct:
                self.consecutive_correct += 1
                if self.consecutive_correct == 2:
                    self.difficulty_level = min(self.difficulty_level + 1, 3)
                    self.consecutive_correct = 0
            else:
                self.consecutive_correct = 0
                self.difficulty_level = max(self.difficulty_level - 1, 1)

    def get_word(self):
        if not self.word_pool[self.difficulty_level]:
            return None, None
        return random.choice(self.word_pool[self.difficulty_level])

# Streamlit UI
st.title("ML-Powered Syllable Splitting Game")

if 'game' not in st.session_state:
    st.session_state.game = MLSyllableSplittingModule(r"C:\Users\Vigasini\Downloads\syllable_dataset1.csv")

if 'current_word' not in st.session_state or 'correct_syllables' not in st.session_state:
    st.session_state.current_word, st.session_state.correct_syllables = st.session_state.game.get_word()
    st.session_state.start_time = time.time()

st.write(f"### Split this word into syllables: **{st.session_state.current_word}**")
user_input = st.text_input("Your answer (use '-' to separate syllables)")

if st.button("Submit"):
    response_time = time.time() - st.session_state.start_time
    correct = int(user_input.strip().lower() == st.session_state.correct_syllables.strip().lower())
    
    if correct:
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Incorrect! The correct answer is: {st.session_state.correct_syllables}")
    
    st.session_state.game.collect_data(st.session_state.game.difficulty_level, correct, response_time)
    st.session_state.game.predict_difficulty(correct, response_time)
    
    st.write(f"🔹 Current Difficulty Level: {st.session_state.game.difficulty_level} | Consecutive Correct: {st.session_state.game.consecutive_correct}")
    
    st.session_state.current_word, st.session_state.correct_syllables = st.session_state.game.get_word()
    st.session_state.start_time = time.time()
