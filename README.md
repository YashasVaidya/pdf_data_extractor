# AI PDF Data Extractor With Human Validation

This Flask-based web application uses AI to extract specific data points from various PDF formats, allowing for human validation and correction before finalizing the output.

## Live Demo

The application is deployed and accessible at:

[https://pdf-data-extractor.onrender.com/](https://pdf-data-extractor.onrender.com/)

## Features

- AI-powered PDF data extraction
- Supports a wide range of PDF formats
- Extracts 10 specific datapoints (5 patient-amount pairs)
- Human validation interface with PDF viewer for corrections
- JSON output of extracted and validated data

## Key Datapoints Extracted

- Patient 1, Amount 1
- Patient 2, Amount 2
- Patient 3, Amount 3
- Patient 4, Amount 4
- Patient 5, Amount 5

## Usage

1. Visit [https://pdf-data-extractor.onrender.com/](https://pdf-data-extractor.onrender.com/)
2. Upload a PDF file using the provided interface
3. Review and validate the extracted data, making corrections if necessary
4. Submit the validated data
5. View the final JSON output

## Local Development

If you want to run the application locally for development:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```
   python run.py
   ```

5. Open a web browser and navigate to `http://localhost:5000`

## Deployment

This application is deployed on Render. See the [documentation](docs/code_explanation.md) for more details on the deployment process.
