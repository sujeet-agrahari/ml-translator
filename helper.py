import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.fonts import addMapping
import os

# from bidi.algorithm import get_display  # For RTL languages if needed


def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def create_translated_pdf(original_file_path, translated_text, output_file_path):
    # Define the path to the font file
    font_path = os.path.join(
        os.path.dirname(__file__), "fonts", "NotoSansDevanagari.ttf"
    )

    # Check if the font file exists
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found at path: {font_path}")

    # Register the Devanagari-supporting font
    pdfmetrics.registerFont(TTFont("NotoSansDevanagari", font_path))

    # Optionally map it to normal/bold/italic/bold-italic
    addMapping("NotoSansDevanagari", 0, 0, "NotoSansDevanagari")  # Normal
    addMapping("NotoSansDevanagari", 1, 0, "NotoSansDevanagari")  # Bold if available
    addMapping("NotoSansDevanagari", 0, 1, "NotoSansDevanagari")  # Italic if available
    addMapping(
        "NotoSansDevanagari", 1, 1, "NotoSansDevanagari"
    )  # Bold-Italic if available

    # Create a canvas
    c = canvas.Canvas(output_file_path, pagesize=letter)
    c.setFont("NotoSansDevanagari", 12)

    # Simplistic line wrapping for the PDF output
    lines = translated_text.split("\n")
    y_position = 750

    for line in lines:
        # Implement proper word wrapping
        wrapped_lines = wrap_text(
            line, 80
        )  # Assume 80 characters per line, adjust as needed
        for wrapped_line in wrapped_lines:
            if y_position < 50:
                c.showPage()
                c.setFont("NotoSansDevanagari", 12)
                y_position = 750
            c.drawString(100, y_position, wrapped_line)
            y_position -= 20

    c.save()


def wrap_text(text, max_chars):
    """
    A simple word-wrap function to split text into lines no longer than `max_chars`.
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) <= max_chars:
            current_line.append(word)
            current_length += len(word) + 1  # +1 for the space
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word) + 1

    if current_line:
        lines.append(" ".join(current_line))

    return lines
