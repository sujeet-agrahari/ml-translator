from transformers import (
    MBartForConditionalGeneration,
    MBart50TokenizerFast,
    T5Tokenizer,
    T5ForConditionalGeneration,
)
import torch

from helper import wrap_text

# Load translation model and tokenizer
translation_model_name = "SnypzZz/Llama2-13b-Language-translate"
translation_model = MBartForConditionalGeneration.from_pretrained(
    translation_model_name
)
translation_tokenizer = MBart50TokenizerFast.from_pretrained(
    translation_model_name, src_lang="en_XX"
)

# Load summarization model and tokenizer
summarization_model_name = "google-t5/t5-base"
summarization_model = T5ForConditionalGeneration.from_pretrained(
    summarization_model_name
)
summarization_tokenizer = T5Tokenizer.from_pretrained(
    summarization_model_name, legacy=False
)

# Ensure the models run on a compatible device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
translation_model.to(device)
summarization_model.to(device)


def translate_text(input_text, target_language, max_length=120):
    """
    Translate input text to the specified target language using MBart model.

    Args:
    input_text (str): The text to translate.
    target_language (str): The target language code (e.g., 'hi_IN').
    max_length (int): Maximum token length for each translation chunk.

    Returns:
    str: The translated text.
    """
    # Tokenize input text
    input_text = input_text.strip()
    if not input_text:
        raise ValueError("Input text is empty.")

    # Split text into chunks based on maximum token length
    text_chunks = wrap_text(input_text, max_length)

    # Initialize list to hold translated chunks
    translated_chunks = []

    for chunk in text_chunks:
        # Tokenize input text chunk
        model_inputs = translation_tokenizer(
            chunk, return_tensors="pt", truncation=True, max_length=max_length
        ).to(device)

        # Get the BOS token ID for the target language
        try:
            bos_token_id = translation_tokenizer.lang_code_to_id[target_language]
        except KeyError:
            raise ValueError(f"Unsupported language code: {target_language}")

        # Generate translation using the model
        generated_tokens = translation_model.generate(
            **model_inputs,
            forced_bos_token_id=bos_token_id,
            max_length=max_length
            + 50,  # Allow for expansion of text during translation
            num_beams=4,  # Use beam search for better quality
            early_stopping=True,  # Stop once the entire text is generated
        )

        # Decode the generated output
        translation = translation_tokenizer.batch_decode(
            generated_tokens, skip_special_tokens=True
        )[0]

        # Append translated chunk to list
        translated_chunks.append(translation.strip())

    # Join the translated chunks
    full_translation = " ".join(translated_chunks)

    return full_translation


def summarize_text(input_text):
    """
    Summarize the input text using T5 model.

    Args:
    input_text (str): The text to summarize.

    Returns:
    str: The summarized text.
    """
    # Add T5-specific task prefix for summarization
    input_text = "summarize: " + input_text

    # Tokenize input text
    # Tokenize the input and convert to PyTorch tensors
    input_ids = summarization_tokenizer.encode(input_text, return_tensors="pt").to(
        device
    )

    # Generate summary using the model
    summary_ids = summarization_model.generate(
        input_ids,
        num_beams=5,  # Increase beam search width
        min_length=20,  # Ensure minimum length of summary
        max_length=60,  # Restrict maximum length
        early_stopping=True,
        repetition_penalty=2.0,  # Penalize repetitions
        temperature=0.7,  # Increase randomness
        top_k=50,  # Limit top-k tokens sampling
        top_p=0.9,  # Use nucleus sampling
        do_sample=True,  # Sample from the top-k tokens
    )

    # Decode the generated summary
    summary = summarization_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
