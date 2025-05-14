import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, render_template, request, jsonify

# Download necessary NLTK data
nltk.download('vader_lexicon')

app = Flask(__name__)
sid = SentimentIntensityAnalyzer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    
    # Analyze sentiment
    scores = sid.polarity_scores(text)
    
    # Determine sentiment category
    compound = scores['compound']
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Format scores for display
    result = {
        'sentiment': sentiment,
        'scores': {
            'positive': f"{scores['pos']:.2f}",
            'neutral': f"{scores['neu']:.2f}",
            'negative': f"{scores['neg']:.2f}",
            'compound': f"{scores['compound']:.2f}"
        },
        'text': text
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5501) 