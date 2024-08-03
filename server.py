# app.py

from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch

# Initialize Flask app
app = Flask(__name__)

# Load the model and tokenizer
model_name = "SnypzZz/Llama2-13b-Language-translate"
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(model_name, src_lang="en_XX")

# Ensure the model runs on a compatible device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# Define translation function
def translate_text(input_text, target_language):
    # Prepare the input text for translation
    model_inputs = tokenizer(input_text, return_tensors="pt").to(device)

    # Get the BOS token ID for the target language
    try:
        bos_token_id = tokenizer.lang_code_to_id[target_language]
    except KeyError:
        raise ValueError(f"Unsupported language code: {target_language}")

    # Generate translation using the model
    generated_tokens = model.generate(**model_inputs, forced_bos_token_id=bos_token_id)

    # Decode the generated output
    translation = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    return translation


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


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
