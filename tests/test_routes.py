import unittest
from app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

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

if __name__ == '__main__':
    unittest.main()