import unittest
from uuid import UUID
import uuid
from pymongo import MongoClient

# Simulated in-memory database
mock_db = {}
"""
create_random_document()

Creates a random MongoDB document with a unique UUID field.

Returns:
    str: The UUID of the newly inserted document.

The document contains the following fields:
- UUID: A version 4 UUID (string format).
- field1: A placeholder field with a predefined value ("random_value_1").
- field2: Another placeholder field with a predefined value ("random_value_2").

The function connects to a MongoDB instance running locally on `localhost:27017`.
It inserts the document into the `test_collection` collection within the `test_database`.

Dependencies:
- MongoDB server must be running and accessible at the default host and port.
- The `pymongo` library must be installed.

Example:
    # Call the function to create and store a random document
    document_uuid = create_random_document()
    print(f"Document created with UUID: {document_uuid}")
"""


def create_random_document():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Ensure MongoDB is running
    db = client.test_database
    collection = db.test_collection

    # Create a random document
    document = {
        "UUID": str(uuid.uuid4()),  # Generate a version 4 UUID
        "field1": "random_value_1",  # Example field
        "field2": "random_value_2"   # Another example field
    }
    
    # Insert the document into the collection
    collection.insert_one(document)
    
    # Return the UUID
    return document["UUID"]
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