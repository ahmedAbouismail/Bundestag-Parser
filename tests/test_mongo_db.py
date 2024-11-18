import unittest
from unittest.mock import MagicMock, patch
from source.mongo_db import sync


class TestMongoDb(unittest.TestCase):
    @patch('source.mongo_db.db', new_callable=MagicMock)
    def test_sync_valid_data(self, mock_db):
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        data = [{"id": 1, "name": "Test"}]
        sync(data, "test_collection")

        # prüfe, on bulk_write wurde aufgerufen
        self.assertTrue(mock_collection.bulk_write.called)
        operations = mock_collection.bulk_write.call_args[0][0]
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]._filter, {"id": 1})

    @patch('source.mongo_db.db', new_callable=MagicMock)
    def test_sync_invalid_data(self, mock_db):
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        data = ["invalid_data"]

        sync(data, "test_collection")

        self.assertFalse(mock_collection.bulk_write.called)


if __name__ == '__main__':
    unittest.main()
