import os
import time
import subprocess
import threading
import webbrowser
from flask import Flask, render_template, redirect

app = Flask(__name__)

# Store subprocess objects
processes = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sentiment')
def sentiment():
    # Open sentiment analysis app in new tab
    webbrowser.open_new_tab('http://localhost:5501')
    return redirect('/')

@app.route('/voice')
def voice():
    # Open voice assistant app in new tab
    webbrowser.open_new_tab('http://localhost:5502')
    return redirect('/')

@app.route('/chatbot')
def chatbot():
    # Open chatbot app in new tab
    webbrowser.open_new_tab('http://localhost:5503')
    return redirect('/')

def start_app(app_path, port):
    """Start a Flask application in a subprocess"""
    os.chdir(app_path)
    process = subprocess.Popen(['python', 'app.py'])
    processes.append(process)
    print(f"Started app in {app_path} on port {port}")

def main():
    # Start each app in a separate thread
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Start sentiment analysis app
    sentiment_thread = threading.Thread(
        target=start_app,
        args=(os.path.join(base_dir, 'sentiment_analysis'), 5501)
    )
    sentiment_thread.daemon = True
    sentiment_thread.start()
    
    # Start voice assistant app
    voice_thread = threading.Thread(
        target=start_app,
        args=(os.path.join(base_dir, 'voice_assistant'), 5502)
    )
    voice_thread.daemon = True
    voice_thread.start()
    
    # Start chatbot app
    chatbot_thread = threading.Thread(
        target=start_app,
        args=(os.path.join(base_dir, 'chatbot'), 5503)
    )
    chatbot_thread.daemon = True
    chatbot_thread.start()
    
    # Wait for apps to start
    time.sleep(2)
    
    # Open main app in browser
    webbrowser.open('http://localhost:5504')
    
    # Run main app
    app.run(port=5504)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down all applications...")
        for process in processes:
            process.terminate() 