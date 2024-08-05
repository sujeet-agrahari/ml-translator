# app.py

from flask import Flask, request, jsonify
from urllib.parse import quote as url_quote
from model import translate_text, summarize_text
import traceback  # Import the traceback module for detailed error logs
from flask_cors import CORS
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)
# Define API endpoint for translation
# Function to translate text within HTML content
def translate_html_content(html_content, target_language):
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup.find_all(text=True):
        # Perform translation only on text nodes
        translated_text = translate_text(element, target_language)
        element.replace_with(translated_text)
    return str(soup)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json

    # Extract input text and target language
    input_text = data.get("input_text")
    target_language = data.get("target_language")
    isHTML = contains_html_tags(input_text);

    if isHTML:
        # If the input text contains HTML tags, translate the text within the tags
        translated_text = translate_html_content(input_text, target_language)
        return jsonify({"translated_text": translated_text})
    if not input_text or not target_language:
        return jsonify({"error": "Please provide input_text and target_language"}), 400
    
    try:
        # Perform translation
        translated_text = translate_text(input_text, target_language)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Define API endpoint for summarization
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json

    # Extract input text
    input_text = data.get("input_text")

    if not input_text:
        return jsonify({"error": "Please provide input_text for summarization"}), 400

    try:
        # Perform summarization
        summarized_text = summarize_text(input_text)
        return jsonify({"summarized_text": summarized_text})
    except Exception as e:
        # Print full stack trace for debugging
        error_trace = traceback.format_exc()  # Get the complete error stack trace
        print(error_trace)  # Log to console, or use a logging library
        return jsonify({"error": str(e)}), 500

def contains_html_tags(input_string):
    soup = BeautifulSoup(input_string, 'html.parser')
    # If the input string is parsed and any tag is found, it means it contains HTML tags
    return bool(soup.find())

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
