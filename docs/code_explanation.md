# Code and Repository Explanation

This document provides an overview of the AI PDF Data Extractor with Human Validation application.

## Live Deployment

The application is currently deployed and accessible at:

[https://pdf-data-extractor.onrender.com/](https://pdf-data-extractor.onrender.com/)

## Repository Structure

```
.
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── utils/
│       ├── __init__.py
│       └── pdf_extractor.py
├── config/
│   └── repo_context_config.json
├── docs/
│   └── code_explanation.md
├── static/
│   ├── js/
│   │   └── main.js
│   └── css/
│       └── styles.css
├── templates/
│   └── index.html
├── tests/
│   ├── __init__.py
│   ├── test_data/
│   │   └── sample_pdf.pdf
│   ├── test_pdf_extractor.py
│   └── test_routes.py
├── .gitignore
├── config.py
├── Procfile
├── README.md
├── requirements.txt
└── run.py
```

## Key Components

1. `app/utils/pdf_extractor.py`: Contains the AI logic for extracting data from PDF files
2. `app/routes.py`: Defines the application routes and handles file uploads, data validation, and JSON output
3. `static/js/main.js`: Manages the client-side interface for PDF viewing and data validation
4. `templates/index.html`: The main HTML template for the application's user interface
5. `config.py`: Stores configuration variables, including AI model settings
6. `requirements.txt`: Lists all Python dependencies, including AI and PDF processing libraries

## How It Works

1. PDF Upload: The user uploads a PDF file through the web interface at [https://pdf-data-extractor.onrender.com/](https://pdf-data-extractor.onrender.com/).
2. Extraction: The `extract_data_from_pdf` function in `pdf_extractor.py` uses AI techniques to identify and extract the 10 required datapoints (5 patient-amount pairs) from the PDF.
3. Data Display: The extracted data is sent to the client-side and displayed in an editable form alongside a PDF viewer.
4. Human Validation: The user can review the extracted data, make corrections if needed, and select the correct location on the PDF for any misextracted data.
5. Data Submission: The user submits the validated data back to the server.
6. JSON Output: The server processes the validated data and returns a JSON output of the final, corrected datapoints.


## Deployment

The application is currently deployed on Render. The deployment process involved:

1. Pushing the code to a GitHub repository.
2. Creating a new Web Service on Render, connected to the GitHub repository.
3. Configuring the deployment settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
4. Setting up environment variables in the Render dashboard, including `SECRET_KEY`.
5. Automatic deployment triggered by pushes to the main branch of the GitHub repository.

For any future updates or redeployments:

1. Make changes to the code locally.
2. Commit and push the changes to GitHub:
   ```
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
3. Render will automatically detect the changes and redeploy the application.

## Testing

To run the tests locally, use the following command:

```
python -m unittest discover tests
```

This will run all the tests in the `tests/` directory, including tests for the AI extraction process and data validation.
