# Dyslexia Learning App

## Overview
This application is designed to help individuals with dyslexia improve their language skills through interactive learning modules. The app includes syllable splitting exercises, sentence formation with a drag-and-drop interface, and dynamic difficulty adjustment based on user performance.

## Features
- **Syllable Splitting**: Users practice breaking words into syllables, with difficulty adapting based on correctness.
- **Sentence Formation**: A drag-and-drop interface where users arrange words to form correct sentences.
- **Dynamic Difficulty Adjustment**: Users must answer correctly twice to advance, and incorrect answers keep them at the current level.
- **OCR-based Form Filling**: Extracts data from PDFs using OCR to automate form filling.

## Tech Stack
- **Frontend**: React (if applicable)
- **Backend**: Python, Streamlit
- **Database**: SQLite or other (if applicable)
- **OCR**: Tesseract or Google Vision API

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Dyslexia-learning-app-main
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit application:
```bash
streamlit run app.py
```

## File Structure
- `app.py` - Main entry point for the Streamlit application.
- `audio.py` - Handles audio processing for the chatbot.
- `config.py` - Configuration settings for the application.
- `create_db.py` - Script for setting up the database.
- `db_config.py` - Database connection settings.
- `phoneme_dataset.csv` - Dataset for phoneme recognition.
- `difficulty_model.pkl` - Model for adjusting difficulty dynamically.

## Requirements
- Python 3.8+
- Streamlit
- OCR libraries (Tesseract or Google Vision API)


