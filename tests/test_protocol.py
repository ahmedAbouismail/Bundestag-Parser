import unittest
from source.protocol import parse_xml, get_all_json


class TestProtocol(unittest.TestCase):
    def setUp(self):
        self.xml_file_path = "data/20195.xml"
        self.test_dir = "data/"  # XML Dateien für get_all_json

    def test_parse_xml_structure(self):
        """testen, ob parse_xml die erwartete JSON-Struktur zurückgibt"""
        result = parse_xml(self.xml_file_path)

        # erwartete Schlüssel im zurückgegebenen JSON
        expected_keys = {"id", "datum", "wahlperiode", "sitzungsnummer", "sitzungsverlauf"}

        # Prüfen, ob alle Schlüssel existieren
        for key in expected_keys:
            self.assertIn(key, result, f"Fehlender Schlüssel in result: {key}")

    def test_parse_xml_content(self):
        """testen, ob parse_xml richtigen Inhalt für bekannte Fielder zurückgibt"""
        result = parse_xml(self.xml_file_path)

        # Inhalt von Feldern prüfen
        self.assertEqual(result["wahlperiode"], '20', "Falsche 'wahlperiode'")
        self.assertEqual(result["sitzungsnummer"], '195', "Falsche 'sitzungsnummer'")
        self.assertEqual(result["datum"], "18.10.2024", "Falsches 'datum'")
        self.assertIsInstance(result["sitzungsverlauf"], list, "'sitzungsverlauf' muss eine List sein")

    def test_get_all_json(self):
        """Test get_all_json """
        results = get_all_json(self.test_dir)

        # Prüfen, ob results eine List ist
        self.assertIsInstance(results, list, "get_all_json muss eine List zurückgeben")

        # Prüfen, ob alle Schlüssel existieren
        for result in results:
            expected_keys = {"id", "datum", "wahlperiode", "sitzungsnummer", "sitzungsverlauf"}
            for key in expected_keys:
                self.assertIn(key, result, f"Fehlender Schlüssel in result: {key}")


if __name__ == "__main__":
    unittest.main()
