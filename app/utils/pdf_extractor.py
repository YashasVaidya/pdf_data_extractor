import re
import fitz
import io

def extract_data_from_pdf(file_stream):
    text = ""
    with fitz.open(stream=file_stream, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    
    data = {}
    patient_pattern = r'Patient\s*(\d)\s*:\s*([\w\s]+?)(?:\n|$)'
    amount_pattern = r'Amount\s*(\d)\s*:\s*\$?([\d,]+(?:\.\d{2})?)'
    
    for number, name in re.findall(patient_pattern, text, re.MULTILINE):
        data[f'patient_{number}'] = name.strip()
    
    for number, amount in re.findall(amount_pattern, text):
        data[f'amount_{number}'] = amount.replace(',', '')
    
    return data