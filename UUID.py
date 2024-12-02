import unittest
from uuid import UUID
from pymongo import MongoClient

# Mock function to be implemented later
def create_random_document():
    pass

class TestMongoDocument(unittest.TestCase):
    def setUp(self):
        self.mongo_client = MongoClient()  # Assuming MongoDB is running locally
        self.db = self.mongo_client.test_database
        self.collection = self.db.test_collection

    def tearDown(self):
        self.collection.drop()  # Clean up the test collection

    def test_document_creation(self):
        # Create a random document
        doc_id = create_random_document()
        self.assertIsInstance(doc_id, str)  # Ensure it returns a string
        
        # Fetch the document from MongoDB
        document = self.collection.find_one({"UUID": doc_id})
        self.assertIsNotNone(document)  # Ensure the document exists in the database
        
        # Validate the UUID format
        try:
            UUID(document["UUID"], version=4)
        except ValueError:
            self.fail("The UUID field is not a valid version 4 UUID.")
        
        # Check other fields
        self.assertIn("field1", document)
        self.assertIn("field2", document)