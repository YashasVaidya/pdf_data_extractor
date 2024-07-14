import re
import fitz
import logging

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
    return text

def extract_data_from_text(text):
    data = {}
    
    # Pattern for "Patient X: Name" (capturing full name)
    patient_pattern = r'Patient\s*(\d)\s*:\s*([\w\s]+?)(?=\s*Patient|\s*Amount|\s*$)'
    amount_pattern = r'Amount\s*(\d)\s*:\s*\$?([\d,]+(?:\.\d{2})?)'
    
    patient_matches = re.findall(patient_pattern, text, re.DOTALL)
    amount_matches = re.findall(amount_pattern, text)
    
    # Process patient matches
    for number, name in patient_matches:
        data[f'patient_{number}'] = name.strip()
    
    # Process amount matches
    for number, amount in amount_matches:
        data[f'amount_{number}'] = amount.replace(',', '')
    
    return data

def process_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    data = extract_data_from_text(text)
    return data