# AI Systems Assignment

This project implements three key components of intelligent systems:

1. **Sentiment Analysis Model** - Identifies and categorizes opinions in text data
2. **Voice Assistant** - Recognizes and responds to voice commands
3. **E-commerce Chatbot** - Simulates customer support for an online store

## Project Structure

```
ai_project/
├── app.py                  # Main application launcher
├── README.md               # This file
├── requirements.txt        # Project dependencies
├── templates/              # Main app templates
│   └── index.html          # Main landing page
├── sentiment_analysis/     # Sentiment Analysis component
│   ├── app.py              # Sentiment analysis application
│   ├── requirements.txt    # Component dependencies
│   └── templates/          # Component templates
│       └── index.html      # Sentiment analysis UI
├── voice_assistant/        # Voice Assistant component
│   ├── app.py              # Voice assistant application
│   ├── requirements.txt    # Component dependencies 
│   └── templates/          # Component templates
│       └── index.html      # Voice assistant UI
└── chatbot/                # E-commerce Chatbot component
    ├── app.py              # Chatbot application
    ├── requirements.txt    # Component dependencies
    └── templates/          # Component templates
        └── index.html      # Chatbot UI
```

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/ai-systems-assignment.git
cd ai-systems-assignment
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r ai_project/requirements.txt
```

## Running the Applications

To run all applications at once:

```
cd ai_project
python app.py
```

This will launch:
- Main application at http://localhost:5003
- Sentiment Analysis at http://localhost:5000
- Voice Assistant at http://localhost:5001
- E-commerce Chatbot at http://localhost:5002

You can also run each component individually:

```
cd ai_project/sentiment_analysis
python app.py
```

## Components Details

### 1. Sentiment Analysis

* Uses NLTK's VADER sentiment analyzer
* Provides positive, negative, neutral, and compound scores
* Visual representation of sentiment scores
* Real-time analysis of user input

### 2. Voice Assistant

* Speech-to-text using SpeechRecognition library
* Pattern matching for command recognition
* Responds to queries about time, date, weather, etc.
* Supports both voice and text input

### 3. E-commerce Chatbot

* Domain-specific knowledge base for e-commerce support
* Handles queries about products, shipping, returns, etc.
* Natural language processing with NLTK
* Interactive UI with typing indicators and suggested questions

## LinkedIn Poster Content

For the LinkedIn post, capture the following screenshots:

1. **Main Application Dashboard**: Shows all three components
2. **Sentiment Analysis**: Show analysis of both positive and negative text examples
3. **Voice Assistant**: Capture the chat interface with sample responses
4. **E-commerce Chatbot**: Show sample interactions about product information, shipping, etc.
5. **Project Architecture**: Include a diagram showing how components interact

Include bullet points highlighting:
- Technologies used (Python, Flask, NLTK, SpeechRecognition)
- Key features of each system
- Learning outcomes from the project
- Future improvement possibilities

## Technologies Used

- Python 3.8+
- Flask web framework
- NLTK for natural language processing
- SpeechRecognition for voice interface
- HTML/CSS/JavaScript for front-end UI

## License

This project is licensed under the MIT License - see the LICENSE file for details. 