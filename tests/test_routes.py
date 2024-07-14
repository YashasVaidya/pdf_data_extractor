import unittest
from app import app
from app.routes import process_pdf
import os
import tempfile

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload_route(self):
        test_pdf_path = 'tests/test_data/Simple_Layout_PDF_Template.pdf'
        with open(test_pdf_path, 'rb') as test_pdf:
            data = {
                'file': (test_pdf, 'test.pdf')
            }
            response = self.app.post('/upload', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.json)

    def test_validate_route(self):
        # First, we need to process a PDF to get a valid record_id
        test_pdf_path = 'tests/test_data/Simple_Layout_PDF_Template.pdf'
        _, record_id = process_pdf(test_pdf_path)
        
        # Now we can test the validate route
        response = self.app.get(f'/validate/{record_id}')
        self.assertEqual(response.status_code, 200)

        # Test POST to validate route
        data = {
            'patient_1': 'John',
            'amount_1': '500.00',
            'patient_2': 'Jane',
            'amount_2': '750.50'
        }
        response = self.app.post(f'/validate/{record_id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json)

if __name__ == '__main__':
    unittest.main()