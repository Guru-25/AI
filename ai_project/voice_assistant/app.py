import os
import time
import json
import random
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)

# Initialize recognizer
recognizer = sr.Recognizer()

# Commands and responses
COMMANDS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "greetings", "howdy"],
        "responses": ["Hello there!", "Hi! How can I help?", "Hey! What can I do for you?"]
    },
    "time": {
        "patterns": ["what time", "current time", "time now"],
        "responses": [f"The current time is {time.strftime('%H:%M:%S')}"]
    },
    "date": {
        "patterns": ["what date", "current date", "date today", "today's date"],
        "responses": [f"Today's date is {time.strftime('%Y-%m-%d')}"]
    },
    "weather": {
        "patterns": ["weather", "temperature", "forecast"],
        "responses": ["I'm sorry, I don't have access to real-time weather data. This is a simulated response."]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "later"],
        "responses": ["Goodbye!", "See you later!", "Have a great day!"]
    },
    "name": {
        "patterns": ["your name", "who are you", "what are you"],
        "responses": ["I'm your voice assistant.", "I'm an AI assistant created for this project."]
    },
    "thanks": {
        "patterns": ["thanks", "thank you", "appreciate"],
        "responses": ["You're welcome!", "Happy to help!", "Anytime!"]
    },
    "help": {
        "patterns": ["help", "assist", "support"],
        "responses": ["I can tell you the time, date, or respond to greetings. Just ask!"]
    }
}

def get_response(text):
    text = text.lower()
    
    for intent, data in COMMANDS.items():
        for pattern in data["patterns"]:
            if pattern in text:
                return random.choice(data["responses"])
    
    return "I'm not sure how to respond to that."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    
    try:
        # Save the uploaded audio temporarily
        temp_filename = "temp_audio.wav"
        audio_file.save(temp_filename)
        
        # Convert the audio to text
        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            
        # Get response
        response = get_response(text)
        
        # Remove temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        
        return jsonify({
            "success": True,
            "text": text,
            "response": response
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/text_command', methods=['POST'])
def text_command():
    data = request.get_json()
    
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    response = get_response(text)
    
    return jsonify({
        "success": True,
        "text": text,
        "response": response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5502) 