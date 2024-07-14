import os
from flask import request, jsonify, render_template, g, current_app
from werkzeug.utils import secure_filename
from app import app
from app.utils.pdf_extractor import process_pdf as pdf_processor
import sqlite3

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
DATABASE = app.config['DATABASE']

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf(file_path):
    with current_app.app_context():
        data = pdf_processor(file_path)
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('''
                INSERT INTO extracted_data 
                (patient_1, amount_1, patient_2, amount_2, patient_3, amount_3, 
                 patient_4, amount_4, patient_5, amount_5, validated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('patient_1'), data.get('amount_1'),
                data.get('patient_2'), data.get('amount_2'),
                data.get('patient_3'), data.get('amount_3'),
                data.get('patient_4'), data.get('amount_4'),
                data.get('patient_5'), data.get('amount_5'),
                False
            ))
            db.commit()
            return data, cursor.lastrowid
        except sqlite3.Error as e:
            current_app.logger.error(f"Database error: {str(e)}")
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
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        final_data, record_id = process_pdf(file_path)
        
        os.remove(file_path)
        
        if final_data and record_id:
            return jsonify({'success': True, 'record_id': record_id})
        else:
            current_app.logger.error(f"Failed to process PDF. final_data: {final_data}, record_id: {record_id}")
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