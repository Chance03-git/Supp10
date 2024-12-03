import unittest
from pymongo import MongoClient

class TestDeleteDocumentByUUID(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.test_database
        self.collection = self.db.test_collection
        self.collection.drop()  # Clear the collection before each test

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

    def test_delete_document(self):
        # Delete the document
        deleted_document = delete_document_by_uuid(self.test_uuid)

        # Verify the document was deleted
        self.assertIsNotNone(deleted_document)
        self.assertEqual(deleted_document["UUID"], self.test_uuid)

        # Verify the document no longer exists in the database
        remaining_document = self.collection.find_one({"UUID": self.test_uuid})
        self.assertIsNone(remaining_document)

    def test_delete_document_not_found(self):
        # Test with a non-existent UUID
        result = delete_document_by_uuid("non-existent-uuid")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
