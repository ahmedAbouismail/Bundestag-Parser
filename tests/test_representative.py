import unittest
import xml.etree.ElementTree as ET
from source.representative import parse_mdb, get_all


class TestRepresentative(unittest.TestCase):
    def setUp(self):
        # Dummy XML fürs Testen von parse_mdb
        self.mdb_sample = "data/representative/MDB_STAMMDATEN.XML"
        # Datei fürs Testen von get_all
        self.test_dir = "data/representative/MDB_STAMMDATEN.XML"

    def test_parse_mdb_structure(self):
        """testen, ob parse_mdb die erwartete JSON-Struktur zurückgibt"""
        # Dummy XML parsen

        tree = ET.parse(self.mdb_sample)
        root = tree.getroot()

        # Extrahiere alle MDB Einträge
        mdb_list = []
        mdb = root.findall("MDB")
        result = parse_mdb(mdb[0])

        # erwartete Schlüssel im zurückgegebenen JSON
        expected_keys = {"id", "vorname", "nachname", "fraktion", "biographie", "wahlperiode"}
        for key in expected_keys:
            self.assertIn(key, result, f"Fehlender Schlüssel in result: {key}")

        # Inhalt von Feldern prüfen
        self.assertEqual(result["id"], "11000001", "Falscher 'id'")
        self.assertEqual(result["vorname"], "Manfred", "Falscher 'vorname'")
        self.assertEqual(result["nachname"], "Abelein", "Falscher 'nachname'")
        self.assertEqual(result["fraktion"], "CDU", "Falscher 'fraktion'")
        self.assertIsInstance(result["biographie"], dict, "'biographie' muss ein Dict sein")
        self.assertIsInstance(result["wahlperiode"], list, "'wahlperiode' muss eine List sein")

    def test_get_all(self):
        """Test get_all"""

        results = get_all(self.test_dir)

        # Prüfen, ob results eine List ist
        self.assertIsInstance(results, list, "get_all muss eine List zurückgeben")

        # Prüfen, ob alle Schlüssel existieren
        for result in results:
            expected_keys = {"id", "vorname", "nachname", "fraktion", "biographie", "wahlperiode"}
            for key in expected_keys:
                self.assertIn(key, result, f"Fehlender Schlüssel in result: {key}")


if __name__ == "__main__":
    unittest.main()
