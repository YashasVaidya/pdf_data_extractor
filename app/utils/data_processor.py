import re

def extract_datapoints(text):
    patterns = {
        'patient_1': r'Patient 1:?\s*(\w+)',
        'amount_1': r'Amount 1:?\s*\$?(\d+(?:\.\d{2})?)',
        'patient_2': r'Patient 2:?\s*(\w+)',
        'amount_2': r'Amount 2:?\s*\$?(\d+(?:\.\d{2})?)',
        'patient_3': r'Patient 3:?\s*(\w+)',
        'amount_3': r'Amount 3:?\s*\$?(\d+(?:\.\d{2})?)',
        'patient_4': r'Patient 4:?\s*(\w+)',
        'amount_4': r'Amount 4:?\s*\$?(\d+(?:\.\d{2})?)',
        'patient_5': r'Patient 5:?\s*(\w+)',
        'amount_5': r'Amount 5:?\s*\$?(\d+(?:\.\d{2})?)'
    }

    datapoints = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            datapoints[key] = match.group(1)
        else:
            datapoints[key] = None
    return datapoints

def handle_layout_variations(text):
    text = re.sub(r'\s+', ' ', text)
    
    layouts = [
        r'Patient (\d+)[\s:]+(\w+)[\s:]+Amount[\s:]+\$?(\d+(?:\.\d{2})?)',
        r'(\w+)[\s:]+Patient (\d+)[\s:]+\$?(\d+(?:\.\d{2})?)',
        r'(\d+)[\s:]+(\w+)[\s:]+\$?(\d+(?:\.\d{2})?)'
    ]
    
    extracted_data = {}
    for layout in layouts:
        matches = re.findall(layout, text, re.IGNORECASE)
        for match in matches:
            patient_num, patient_name, amount = match
            extracted_data[f'patient_{patient_num}'] = patient_name
            extracted_data[f'amount_{patient_num}'] = amount
    
    return extracted_data

def process_data(text):
    datapoints = extract_datapoints(text)
    layout_data = handle_layout_variations(text)
    final_data = {**datapoints, **layout_data}
    return final_data