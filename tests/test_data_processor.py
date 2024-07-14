import unittest
from app.utils.data_processor import process_data

class TestDataProcessor(unittest.TestCase):
    def test_process_data(self):
        test_cases = [
            ("Patient 1: John Doe Amount 1: $500.00", {'patient_1': 'John Doe', 'amount_1': '500.00'}),
            ("1: Alice $300.25 2: Bob $750.50", {'patient_1': 'Alice', 'amount_1': '300.25', 'patient_2': 'Bob', 'amount_2': '750.50'}),
            ("Charlie Davis Patient 5 Amount: 980.00", {'patient_5': 'Charlie Davis', 'amount_5': '980.00'}),
            ("Patient 3: Eve Johnson", {'patient_3': 'Eve Johnson'}),
            ("4: David Amount 4: $1,234.56", {'patient_4': 'David', 'amount_4': '1234.56'}),
            ("Patient 2: Jane Smith\nAmount 2: $750.50", {'patient_2': 'Jane Smith', 'amount_2': '750.50'}),
            ("6: Frank White $2,000.00", {'patient_6': 'Frank White', 'amount_6': '2000.00'})
        ]
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = process_data(text)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()