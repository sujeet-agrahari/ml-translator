# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from model import translate_text, summarize_text
import traceback  # Import the traceback module for detailed error logs

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all origins
CORS(app)  # Allow all origins


# Define API endpoint for translation
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json

    # Extract input text and target language
    input_text = data.get("input_text")
    target_language = data.get("target_language")

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


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
