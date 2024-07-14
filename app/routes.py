from flask import request, jsonify, render_template
from app import app
from app.utils.pdf_extractor import extract_data_from_pdf
import io
import logging

logging.basicConfig(level=logging.DEBUG)

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
        data = extract_data_from_pdf(file_stream)
        logging.debug(f"Extracted data: {data}")
        return jsonify({'success': True, 'extracted_data': data})
    return jsonify({'error': 'File type not allowed'})

@app.route('/validate', methods=['POST'])
def validate_data():
    data = request.json
    logging.debug(f"Validated data: {data}")
    return jsonify({'success': True, 'final_data': data})