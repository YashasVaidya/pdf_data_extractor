import fitz  # PyMuPDF
import os
import re
import pytesseract
from PIL import Image
import io
import logging
import sqlite3
from flask import Flask, request, jsonify, render_template, g
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
DATABASE = 'pdf_data.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def process_pdf(file_path):
    try:
        extracted_text = extract_text_from_pdf(file_path)
        datapoints = extract_datapoints(extracted_text)
        layout_data = handle_layout_variations(extracted_text)
        final_data = {**datapoints, **layout_data}
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO extracted_data 
            (patient_1, amount_1, patient_2, amount_2, patient_3, amount_3, 
             patient_4, amount_4, patient_5, amount_5, validated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            final_data.get('patient_1'), final_data.get('amount_1'),
            final_data.get('patient_2'), final_data.get('amount_2'),
            final_data.get('patient_3'), final_data.get('amount_3'),
            final_data.get('patient_4'), final_data.get('amount_4'),
            final_data.get('patient_5'), final_data.get('amount_5'),
            False
        ))
        db.commit()
        
        return final_data, cursor.lastrowid
    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        final_data, record_id = process_pdf(file_path)
        
        os.remove(file_path)
        
        if final_data and record_id:
            return jsonify({'success': True, 'record_id': record_id})
        else:
            return jsonify({'error': 'Failed to process PDF'})
    return jsonify({'error': 'File type not allowed'})

@app.route('/validate/<int:record_id>', methods=['GET', 'POST'])
def validate_data(record_id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            UPDATE extracted_data
            SET patient_1=?, amount_1=?, patient_2=?, amount_2=?, 
                patient_3=?, amount_3=?, patient_4=?, amount_4=?, 
                patient_5=?, amount_5=?, validated=?
            WHERE id=?
        ''', (
            data['patient_1'], data['amount_1'],
            data['patient_2'], data['amount_2'],
            data['patient_3'], data['amount_3'],
            data['patient_4'], data['amount_4'],
            data['patient_5'], data['amount_5'],
            True, record_id
        ))
        db.commit()
        return jsonify({'success': True})
    
    cursor.execute('SELECT * FROM extracted_data WHERE id=?', (record_id,))
    data = cursor.fetchone()
    if data:
        return render_template('validate.html', data=dict(zip([column[0] for column in cursor.description], data)))
    return jsonify({'error': 'Record not found'})

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)