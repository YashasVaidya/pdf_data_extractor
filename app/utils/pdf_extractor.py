import fitz
import pytesseract
from PIL import Image
import io
import logging

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
            
            if not text.strip():
                for page in doc:
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img)
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
    return text