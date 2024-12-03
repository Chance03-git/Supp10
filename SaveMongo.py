import unittest
from pymongo import MongoClient

class TestSaveMongoDocument(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.test_database
        self.collection = self.db.test_collection
        self.collection.drop()  # Clear collection before each test

    def tearDown(self):
        self.collection.drop()  # Clean up after each test

    def test_save_document(self):
        document = {"name": "Jane Doe", "email": "jane.doe@example.com"}
        doc_id = save_mongo_document(document)
        
        # Verify document exists in the database
        saved_doc = self.collection.find_one({"_id": doc_id})
        self.assertIsNotNone(saved_doc)
        self.assertEqual(saved_doc["name"], "Jane Doe")
        self.assertEqual(saved_doc["email"], "jane.doe@example.com")

if __name__ == "__main__":
    unittest.main()