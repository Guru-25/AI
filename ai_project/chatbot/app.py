import random
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from flask import Flask, render_template, request, jsonify

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)
lemmatizer = WordNetLemmatizer()

# E-commerce chatbot knowledge base
ecommerce_kb = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "greetings", "howdy", "good morning", "good afternoon", "good evening"],
        "responses": [
            "Hello! Welcome to our online store. How can I assist you today?",
            "Hi there! I'm here to help with your shopping needs. What can I do for you?",
            "Hey! Thanks for reaching out. What are you looking for today?"
        ]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "see you later", "farewell", "until next time"],
        "responses": [
            "Goodbye! Thanks for visiting our store!",
            "Have a great day! Come back soon!",
            "Thank you for shopping with us. Goodbye!"
        ]
    },
    "thanks": {
        "patterns": ["thanks", "thank you", "appreciate it", "thank you very much", "thanks a lot"],
        "responses": [
            "You're welcome! Is there anything else I can help you with?",
            "Happy to help! Let me know if you need anything else.",
            "My pleasure! Feel free to ask if you have any other questions."
        ]
    },
    "product_info": {
        "patterns": ["product information", "product details", "tell me about", "specifications", "features", "what is"],
        "responses": [
            "I'd be happy to provide information about our products. Could you specify which product you're interested in?",
            "Our products come with detailed descriptions and specifications. Which product would you like to know more about?",
            "You can find product information on the product page. Would you like me to help you find a specific product?"
        ]
    },
    "pricing": {
        "patterns": ["price", "cost", "how much", "pricing", "discount", "offer", "deal", "sale"],
        "responses": [
            "Our prices are competitive and we often have special offers. Which product's price are you interested in?",
            "We have various price ranges depending on the product category. What specific item are you looking for?",
            "You can find the pricing information on each product page. Is there a specific product you're inquiring about?"
        ]
    },
    "shipping": {
        "patterns": ["shipping", "delivery", "when will I receive", "shipping cost", "shipping time", "delivery time", "tracking"],
        "responses": [
            "We offer standard shipping (3-5 business days) and express shipping (1-2 business days). Shipping costs depend on your location and the chosen shipping method.",
            "Orders are typically processed within 24 hours and shipped afterward. You'll receive a tracking number once your order ships.",
            "Shipping times vary depending on your location. You can track your order using the tracking number provided in your shipping confirmation email."
        ]
    },
    "returns": {
        "patterns": ["return", "refund", "exchange", "return policy", "money back", "damaged", "wrong item"],
        "responses": [
            "We have a 30-day return policy. If you're not satisfied with your purchase, you can return it in its original condition for a full refund or exchange.",
            "To initiate a return, please go to the 'My Orders' section of your account and select the 'Return' option for the relevant item.",
            "If you received a damaged or incorrect item, please contact us immediately with photos, and we'll arrange for a replacement or refund."
        ]
    },
    "payment": {
        "patterns": ["payment", "payment methods", "credit card", "debit card", "paypal", "pay", "checkout", "payment issue"],
        "responses": [
            "We accept various payment methods including credit/debit cards, PayPal, and bank transfers. All transactions are secure and encrypted.",
            "Having trouble with payment? Please ensure your payment details are correct or try a different payment method.",
            "For payment-related issues, you can contact our support team directly at payment@example.com."
        ]
    },
    "account": {
        "patterns": ["account", "log in", "login", "password reset", "forgot password", "sign up", "register", "profile"],
        "responses": [
            "You can create an account or log in by clicking on the 'Account' icon at the top right of our website.",
            "To reset your password, click on 'Forgot Password' on the login page, and we'll send you instructions via email.",
            "Your account gives you access to order history, saved addresses, and a faster checkout experience."
        ]
    },
    "order_status": {
        "patterns": ["order status", "where is my order", "track order", "order confirmation", "order history", "cancel order"],
        "responses": [
            "You can check your order status in the 'My Orders' section of your account. There you'll find tracking information and delivery updates.",
            "If you haven't received a confirmation email, please check your spam folder or contact our customer service.",
            "To cancel an order, please go to 'My Orders' and select the 'Cancel' option if the order hasn't been shipped yet."
        ]
    },
    "product_recommendations": {
        "patterns": ["recommend", "suggestion", "what do you recommend", "best products", "popular items", "trending"],
        "responses": [
            "I'd be happy to recommend products based on your preferences. What type of item are you looking for?",
            "Our current bestsellers include our premium headphones, smart home devices, and organic skincare products. Would you like more information on any of these?",
            "For personalized recommendations, I'd need to know more about your preferences or needs. Could you tell me what you're looking for?"
        ]
    },
    "contact": {
        "patterns": ["contact", "speak to human", "customer service", "representative", "phone number", "email", "chat"],
        "responses": [
            "You can contact our customer service team via email at support@example.com or by phone at 1-800-123-4567, Monday to Friday, 9 AM to 6 PM EST.",
            "If you'd prefer to speak with a human representative, please call us at 1-800-123-4567 or use the 'Live Chat' option during business hours.",
            "Our support team is available to assist you via email, phone, or live chat. Would you like me to provide contact details?"
        ]
    },
    "fallback": {
        "patterns": [],
        "responses": [
            "I'm not sure I understand. Could you please rephrase your question?",
            "I don't have information about that yet. Would you like to ask something else about our products or services?",
            "I'm still learning and couldn't understand your request. Could you try asking in a different way or contact our customer service for assistance?"
        ]
    }
}

def preprocess_text(text):
    """Tokenize and lemmatize input text"""
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def get_response(user_input):
    """Find the most appropriate response for the user input"""
    processed_input = preprocess_text(user_input)
    
    # Calculate similarity score for each intent
    max_score = 0
    selected_intent = "fallback"
    
    for intent, data in ecommerce_kb.items():
        if intent == "fallback":
            continue
            
        score = 0
        for pattern in data["patterns"]:
            pattern_tokens = preprocess_text(pattern)
            
            # Calculate simple match score
            for token in processed_input:
                if token in pattern_tokens:
                    score += 1
            
        # Normalize score
        if score > 0:
            score = score / len(processed_input)
            
        if score > max_score:
            max_score = score
            selected_intent = intent
    
    # If confidence is too low, use fallback
    if max_score < 0.2:
        selected_intent = "fallback"
    
    # Return a random response from the selected intent
    return random.choice(ecommerce_kb[selected_intent]["responses"])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def process_message():
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    user_message = data['message']
    bot_response = get_response(user_message)
    
    return jsonify({
        "response": bot_response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5503) 