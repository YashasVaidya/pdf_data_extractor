import unittest
from app.utils.pdf_extractor import extract_text_from_pdf, extract_data_from_text, process_pdf

class TestPDFExtractor(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        file_paths = [
            'tests/test_data/Hospital_Financial_Report.pdf',
            'tests/test_data/Patient_Payment_Summary.pdf',
            'tests/test_data/Medical_Billing_Statement.pdf'
        ]
        for file_path in file_paths:
            with self.subTest(file_path=file_path):
                text = extract_text_from_pdf(file_path)
                self.assertIsNotNone(text)
                self.assertNotEqual(text.strip(), "")

    def test_extract_data_from_text(self):
        test_cases = [
            (
                "Hospital Financial Report\nPatient 1\nName Amount\nLuke Skywalker $2,345.67\nPatient 2\nName Amount\nHan Solo $1,234.56\nPatient 3\nName Amount\nHermione Granger $876.54\nPatient 4\nName Amount\nTony Stark $4,321.00\nPatient 5\nName Amount\nBruce Wayne $9,876.54",
                {
                    'patient_1': 'Luke Skywalker', 'amount_1': '2345.67',
                    'patient_2': 'Han Solo', 'amount_2': '1234.56',
                    'patient_3': 'Hermione Granger', 'amount_3': '876.54',
                    'patient_4': 'Tony Stark', 'amount_4': '4321.00',
                    'patient_5': 'Bruce Wayne', 'amount_5': '9876.54'
                }
            ),
            (
                "Patient Payment Summary\nPatient 1: John Doe\nAmount 1: $500.00\nPatient 2: Jane Smith\nAmount 2: $750.50\nPatient 3: Bob Johnson\nAmount 3: $1,200.75\nPatient 4: Alice Brown\nAmount 4: $300.25\nPatient 5: Charlie Davis\nAmount 5: $980.00",
                {
                    'patient_1': 'John Doe', 'amount_1': '500.00',
                    'patient_2': 'Jane Smith', 'amount_2': '750.50',
                    'patient_3': 'Bob Johnson', 'amount_3': '1200.75',
                    'patient_4': 'Alice Brown', 'amount_4': '300.25',
                    'patient_5': 'Charlie Davis', 'amount_5': '980.00'
                }
            ),
            (
                "Medical Billing Statement\nPatient 1: Sarah Connor\nAmount Due: $1,234.56\nPatient 2: John McClane\nAmount Due: $987.65\nPatient 3: Ellen Ripley\nAmount: $543.21\nPatient 4: Marty McFly\nAmount: $876.54\nPatient 5: Leia Organa\nAmount: $321.98",
                {
                    'patient_1': 'Sarah Connor', 'amount_1': '1234.56',
                    'patient_2': 'John McClane', 'amount_2': '987.65',
                    'patient_3': 'Ellen Ripley', 'amount_3': '543.21',
                    'patient_4': 'Marty McFly', 'amount_4': '876.54',
                    'patient_5': 'Leia Organa', 'amount_5': '321.98'
                }
            ),
        ]
        for text, expected in test_cases:
            with self.subTest(text=text):
                data = extract_data_from_text(text)
                self.assertEqual(data, expected)

    def test_process_pdf(self):
        file_paths = [
            'tests/test_data/Hospital_Financial_Report.pdf',
            'tests/test_data/Patient_Payment_Summary.pdf',
            'tests/test_data/Medical_Billing_Statement.pdf'
        ]
        for file_path in file_paths:
            with self.subTest(file_path=file_path):
                data = process_pdf(file_path)
                self.assertIsInstance(data, dict)
                self.assertEqual(len(data), 10)  # 5 patients and 5 amounts
                for i in range(1, 6):
                    self.assertIn(f'patient_{i}', data)
                    self.assertIn(f'amount_{i}', data)

if __name__ == '__main__':
    unittest.main()