import unittest
from pymongo import MongoClient

class TestFindMongoDocumentByUUID(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.test_database
        self.collection = self.db.test_collection
        self.collection.drop()  # Clear collection before each test

        # Insert a test document
        self.test_uuid = "123e4567-e89b-12d3-a456-426614174000"
        self.test_document = {
            "UUID": self.test_uuid,
            "name": "Test User",
            "email": "test.user@example.com"
        }
        self.collection.insert_one(self.test_document)

    def tearDown(self):
        self.collection.drop()  # Clean up after each test

    def test_find_document_by_uuid(self):
        # Find the document by UUID
        document = find_mongo_document_by_uuid(self.test_uuid)
        self.assertIsNotNone(document)
        self.assertEqual(document["UUID"], self.test_uuid)
        self.assertEqual(document["name"], "Test User")
        self.assertEqual(document["email"], "test.user@example.com")

    def test_find_document_by_uuid_not_found(self):
        # Test for a non-existent UUID
        document = find_mongo_document_by_uuid("non-existent-uuid")
        self.assertIsNone(document)

if __name__ == "__main__":
    unittest.main()
