
import unittest
from main import process_crime_data

class CrimeDataParserTest(unittest.TestCase):

    def test_process_crime_data(self):
        # Sample input data for testing
        sample_data = [
            {"narrative": "Test Crime", "report_date": "2025-01-01", "offense_date": "2025-01-01", "latitude": 28.5383, "longitude": -81.3792},
            {"narrative": "Another Crime", "report_date": "2025-01-02", "offense_date": "2025-01-02", "latitude": 29.5383, "longitude": -80.3792}
        ]
        
        processed_output = process_crime_data(sample_data)
        
        # Verify that the thorn character is present and the data is formatted correctly
        self.assertIn("\u00fe", processed_output)
        self.assertTrue(processed_output.startswith("Test Crime"))
        self.assertTrue(processed_output.endswith("-80.3792"))
    
    def test_empty_data_input(self):
        processed_output = process_crime_data([])
        self.assertEqual(processed_output, "")

if __name__ == "__main__":
    unittest.main()
