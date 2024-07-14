import unittest
from app.utils.pdf_extractor import extract_data_from_pdf

class TestPDFExtractor(unittest.TestCase):
    def test_extract_data_from_pdf(self):
        file_path = 'tests/test_data/Simple_Layout_PDF_Template.pdf'
        expected_data = {
            'patient_1': 'John Doe', 'amount_1': '500.00',
            'patient_2': 'Jane Smith', 'amount_2': '750.50',
            'patient_3': 'Bob Johnson', 'amount_3': '1200.75',
            'patient_4': 'Alice Brown', 'amount_4': '300.25',
            'patient_5': 'Charlie Davis', 'amount_5': '980.00'
        }
        data = extract_data_from_pdf(file_path)
        self.assertEqual(data, expected_data)

if __name__ == '__main__':
    unittest.main()