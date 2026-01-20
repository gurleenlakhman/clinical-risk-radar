import re
import pandas as pd
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    """
    Clean clinical text:
    - lowercase
    - remove special characters
    - normalize whitespace
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_text(text):
    """
    Tokenize and lemmatize clinical text using spaCy
    """
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and len(token) > 2
    ]
    return tokens


def preprocess_notes(input_path, output_path):
    """
    Full preprocessing pipeline:
    - Load raw notes
    - Clean text
    - Tokenize & lemmatize
    - Save processed dataset
    """
    df = pd.read_csv(input_path)

    df["clean_text"] = df["note_text"].apply(clean_text)
    df["tokens"] = df["clean_text"].apply(tokenize_text)

    df.to_csv(output_path, index=False)
    print(f"Preprocessed dataset saved to {output_path}")
