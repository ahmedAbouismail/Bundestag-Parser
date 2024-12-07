import unittest
import os
import json
from unittest.mock import patch
from source.protocol import parse_xml as parse_protocol
from source.representative import parse_mdb as parse_representative
from source.data_cleaning import clean_parsed_json


class TestDataCleaning(unittest.TestCase):

    def setUp(self):
        """Set up paths for test data."""
        self.protocols_path = "./data/protocols"
        self.representative_path = "./data/representative"
        self.data_cleaning = "./logs/data_cleaning"

        # Ensure the log directory exists
        os.makedirs(self.data_cleaning, exist_ok=True)

    def read_json(self, file_path):
        """Utility function to read a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_clean_protocols(self):
        """Test cleaning of protocols JSON data."""
        protocol_files = [
            os.path.join(self.protocols_path, file)
            for file in os.listdir(self.protocols_path) if file.endswith('.xml')
        ]

        for protocol_file in protocol_files:
            # Parse protocol XML
            parsed_data = parse_protocol(protocol_file)
            # Clean parsed data
            with patch('source.data_cleaning.log_change', lambda *args, **kwargs: None):  # Disable logging
                cleaned_data = clean_parsed_json(parsed_data)

            # Ensure cleaned data has no non-printable characters
            for key, value in cleaned_data.items():
                if isinstance(value, str):
                    self.assertNotRegex(value, r'[\x00-\x1F\x7F]',
                                        f"Non-printable characters found in {key}")

    def test_clean_representative(self):
        """Test cleaning of representative JSON data."""
        representative_files = [
            os.path.join(self.representative_path, file)
            for file in os.listdir(self.representative_path) if file.endswith('.xml')
        ]

        for representative_file in representative_files:
            # Parse representative XML
            parsed_data = parse_representative(representative_file)
            # Clean parsed data
            with patch('data_cleaning.log_change', lambda *args, **kwargs: None):  # Disable logging
                cleaned_data = clean_parsed_json(parsed_data)

            # Ensure cleaned data has no non-printable characters
            for key, value in cleaned_data.items():
                if isinstance(value, str):
                    self.assertNotRegex(value, r'[\x00-\x1F\x7F]',
                                        f"Non-printable characters found in {key}")


if __name__ == '__main__':
    unittest.main()
