import csv
import random
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from flask import url_for

app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Function to load advices from CSV file
def load_advices_from_csv(filename):
    advices = {'positive': [], 'negative': [], 'neutral': []}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            advices[row['Type']].append(row['Advice'])
    return advices

# Load advices from CSV file
advices_file = "sample_advices.csv"
sample_advices = load_advices_from_csv(advices_file)

# Function to classify sentiment
def classify_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    if sentiment_score >= 0.05:
        return 'positive'
    elif sentiment_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# Function to provide advice based on sentiment
def get_advice(sentiment):
    return random.choice(sample_advices[sentiment])

# Route for the home page
@app.route('/')
def index():
    return render_template('blog.html')

# Route for processing user input and returning advice
@app.route('/get_advice', methods=['POST'])
def get_advice_api():
    user_input = request.form['user_input']
    if not user_input.strip():
        return jsonify({'error': 'Please enter your feelings.'}), 400
    sentiment = classify_sentiment(user_input)
    advice = get_advice(sentiment)
    return jsonify({'advice': advice})

if __name__ == '__main__':
    app.run(debug=True)
