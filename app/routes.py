from flask import request, jsonify, render_template, g
from app import app
from app.utils.pdf_extractor import process_pdf
import sqlite3
import io
import logging

logging.basicConfig(level=logging.DEBUG)

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
    if file and file.filename.lower().endswith('.pdf'):
        file_stream = io.BytesIO(file.read())
        data = process_pdf(file_stream)
        logging.debug(f"Extracted data: {data}")
        return jsonify({'success': True, 'extracted_data': data})
    return jsonify({'error': 'File type not allowed'})

@app.route('/validate', methods=['POST'])
def validate_data():
    data = request.json
    logging.debug(f"Validated data: {data}")
    # Here you would typically save the validated data to your database
    # For this example, we're just returning the data as-is
    return jsonify({'success': True, 'final_data': data})