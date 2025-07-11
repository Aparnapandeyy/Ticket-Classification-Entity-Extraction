# -*- coding: utf-8 -*-
"""Ticket Classification & Entity Extraction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T6dI_USl3zn-gmckVVFaV_MjYDDmue4N

#**TASK 1**
#**Objective:**
Develop a machine learning pipeline that classifies customer support tickets by their issue
type and urgency level, and extracts key entities (e.g., product names, dates, complaint
keywords). The file (ai_dev_assignment_tickets_complex_1000 ) is provided.

# Step 1: Setup & Preprocessing
"""

#Step 1: Setup & Preprocessing
# Install and import required libraries
!pip install nltk scikit-learn pandas openpyxl --quiet

import pandas as pd
import numpy as np
import re
import nltk
import string

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

"""# Step 2: Load Dataset"""

#Step 2: Load Dataset
# Load the Excel file
file_path = '/content/ai_dev_assignment_tickets_complex_1000 (2).xls'
df = pd.read_excel(file_path)

# Quick look
df.head()

"""#  Step 3 Preprocessing Function"""

# Step 3 Preprocessing Function
# Text cleaner function
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Apply cleaning
df['clean_text'] = df['ticket_text'].apply(clean_text)

# Drop rows with missing labels
df.dropna(subset=['issue_type', 'urgency_level'], inplace=True)

"""# Step 4: Feature Engineering + Model Training"""

#Step 4: Feature Engineering + Model Training
from sklearn.feature_extraction.text import TfidfVectorizer

# TF-IDF Vectorizer for cleaned ticket text
tfidf = TfidfVectorizer(max_features=1000)
X_tfidf = tfidf.fit_transform(df['clean_text'])

def get_sentiment(text):
    if pd.isnull(text):
        return 0.0
    return TextBlob(str(text)).sentiment.polarity

df['sentiment'] = df['ticket_text'].apply(get_sentiment)

def get_sentiment_safe(text):
    try:
        text = str(text)
        return TextBlob(text).sentiment.polarity
    except:
        return 0.0

# Replace any missing ticket_text with empty string first
df['ticket_text'] = df['ticket_text'].fillna("")

# Now apply the robust sentiment function
df['sentiment'] = df['ticket_text'].apply(get_sentiment_safe)

from textblob import TextBlob
!pip install textblob --quiet

# Sentiment polarity score
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Add length and sentiment features
df['ticket_length'] = df['ticket_text'].apply(lambda x: len(str(x)))
df['sentiment'] = df['ticket_text'].apply(get_sentiment)

# Normalize extra features
extra_features = df[['ticket_length', 'sentiment']].values

from scipy.sparse import hstack

X = hstack([X_tfidf, extra_features])

from sklearn.preprocessing import LabelEncoder

# Encode issue_type
issue_encoder = LabelEncoder()
df['issue_encoded'] = issue_encoder.fit_transform(df['issue_type'])

# Encode urgency_level
urgency_encoder = LabelEncoder()
df['urgency_encoded'] = urgency_encoder.fit_transform(df['urgency_level'])

# Split for issue type classification
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(
    X, df['issue_encoded'], test_size=0.2, random_state=42, stratify=df['issue_encoded'])

# Split for urgency level classification
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(
    X, df['urgency_encoded'], test_size=0.2, random_state=42, stratify=df['urgency_encoded'])

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Model 1: Issue Type Classifier
model_issue = LogisticRegression(max_iter=1000)
model_issue.fit(X_train_1, y_train_1)
y_pred_1 = model_issue.predict(X_test_1)

# Model 2: Urgency Classifier
model_urgency = LogisticRegression(max_iter=1000)
model_urgency.fit(X_train_2, y_train_2)
y_pred_2 = model_urgency.predict(X_test_2)

# Evaluation
print("🔹 Issue Type Classification Report:")
print(classification_report(y_test_1, y_pred_1, target_names=issue_encoder.classes_))

print("🔹 Urgency Level Classification Report:")
print(classification_report(y_test_2, y_pred_2, target_names=urgency_encoder.classes_))

"""# Step 5: Entity Extraction"""

#Step 5: Entity Extraction
# Sample complaint-related keywords (expandable)
complaint_keywords = [
    "broken", "damaged", "late", "delayed", "missing", "not working", "error",
    "issue", "cracked", "defective", "problem", "fault", "refund", "cancel"
]

# Create a list of known products from the dataset
product_list = df['product'].dropna().unique().tolist()
product_list = [str(p).lower() for p in product_list]

import re
from datetime import datetime

def extract_entities(text):
    entities = {"product": None, "dates": [], "keywords": []}
    if not text or not isinstance(text, str):
        return entities

    # Convert to lowercase
    text_lower = text.lower()

    # Extract product name if present
    for product in product_list:
        if product in text_lower:
            entities["product"] = product
            break

    # Extract dates (simple regex for DD/MM/YYYY or DD-MM-YYYY or Month DD)
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s\d{1,2}\b'
    ]
    for pattern in date_patterns:
        matches = re.findall(pattern, text_lower)
        entities["dates"].extend(matches)

    # Extract complaint keywords
    for word in complaint_keywords:
        if word in text_lower:
            entities["keywords"].append(word)

    return entities

# Apply on full dataset (optional preview)
df['entities'] = df['ticket_text'].apply(extract_entities)

# Preview
df[['ticket_text', 'entities']].head()

def analyze_ticket(ticket_text):
    return {
        "issue_type": ...,  # predicted
        "urgency_level": ...,  # predicted
        "entities": ...  # extracted
    }

"""# Step 6: Integrated Inference Function"""

#Step 6: Integrated Inference Function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

def analyze_ticket(ticket_text):
    # Handle edge case
    if not ticket_text or not isinstance(ticket_text, str):
        return {"error": "Invalid input text"}

    # Preprocess
    clean = preprocess_text(ticket_text)
    tfidf_vector = tfidf.transform([clean])

    # Extra features
    length = len(ticket_text)
    sentiment = get_sentiment_safe(ticket_text)
    extra = np.array([[length, sentiment]])

    # Combine
    from scipy.sparse import hstack
    full_input = hstack([tfidf_vector, extra])

    # Predict
    issue_pred = model_issue.predict(full_input)[0]
    urgency_pred = model_urgency.predict(full_input)[0]

    # Decode labels
    issue_label = issue_encoder.inverse_transform([issue_pred])[0]
    urgency_label = urgency_encoder.inverse_transform([urgency_pred])[0]

    # Entity extraction
    entities = extract_entities(ticket_text)

    # Final Output
    return {
        "issue_type": issue_label,
        "urgency_level": urgency_label,
        "entities": entities
    }

sample_text = "My washing machine stopped working on 15/06/2025. I need a replacement urgently. It’s broken."

result = analyze_ticket(sample_text)
print(result)

"""# Step 7: Gradio Interface"""

#Step 7: Gradio Interface
!pip install gradio --quiet
import gradio as gr

def gradio_interface(ticket_text):
    result = analyze_ticket(ticket_text)

    # Format nicely for display
    issue = result.get('issue_type', 'N/A')
    urgency = result.get('urgency_level', 'N/A')
    entities = result.get('entities', {})

    entity_text = (
        f"🛍️ Product: {entities.get('product', 'None')}\n"
        f"📅 Dates: {', '.join(entities.get('dates', [])) or 'None'}\n"
        f"⚠️ Keywords: {', '.join(entities.get('keywords', [])) or 'None'}"
    )

    return issue, urgency, entity_text

demo = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=5, placeholder="Paste a customer support ticket here..."),
    outputs=[
        gr.Label(label="Predicted Issue Type"),
        gr.Label(label="Predicted Urgency Level"),
        gr.Textbox(label="Extracted Entities")
    ],
    title="🎫 Smart Ticket Analyzer",
    description="Classifies support ticket by issue type & urgency, and extracts key entities using classical ML and NLP."
)

demo.launch()

"""you can put here this and check "My new refrigerator stopped cooling completely since yesterday. It was delivered on 15/06/2025. I need a technician urgently!"

"""





