# app.py

from flask import Flask, request, jsonify, send_file
from model import translate_text, summarize_text
import traceback  # Import the traceback module for detailed error logs
from helper import create_translated_pdf, extract_text_from_pdf
import os
from transformers import MBart50TokenizerFast

# Initialize Flask app
app = Flask(__name__)

# Load mBART tokenizer
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)


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
        # Print full stack trace for debugging
        error_trace = traceback.format_exc()
        print(error_trace)  # Log to console or use a logging library
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


# Define API endpoint for PDF translation
@app.route("/translate-pdf", methods=["POST"])
def translate_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"error": "Please upload a PDF file"}), 400

    target_language = request.form.get("target_language", "es_XX")  # Default to Spanish

    # Validate language code
    if target_language not in tokenizer.lang_code_to_id:
        return jsonify({"error": "Invalid language code provided"}), 400

    pdf_file = request.files["pdf_file"]
    pdf_path = os.path.join("/tmp", pdf_file.filename)
    pdf_file.save(pdf_path)

    try:
        # Extract text from the original PDF
        original_text = extract_text_from_pdf(pdf_path)

        # Translate the extracted text
        translated_text = translate_text(original_text, target_language)
        print(translated_text)

        # Create a translated PDF with the translated text
        translated_pdf_path = os.path.join("/tmp", f"translated_{pdf_file.filename}")
        create_translated_pdf(pdf_path, translated_text, translated_pdf_path)

        # Return the translated PDF file as an attachment
        return send_file(translated_pdf_path, as_attachment=True)

    except Exception as e:
        # Print full stack trace for debugging
        error_trace = traceback.format_exc()
        print(error_trace)  # Log to console or use a logging library
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
