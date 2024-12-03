import unittest
from pymongo import MongoClient

def save_mongo_document(document, db_name="test_database", collection_name="test_collection"):
    """
    Saves a MongoDB document to the specified database and collection.

    Args:
        document (dict): The document to save. Must be a valid dictionary.
        db_name (str, optional): The name of the database. Defaults to "test_database".
        collection_name (str, optional): The name of the collection. Defaults to "test_collection".

    Returns:
        str: The unique identifier (_id) of the inserted document as a string.

    Raises:
        ValueError: If the document is not a valid dictionary.
        Exception: If the MongoDB insertion fails for any reason.
    """
    # Validate the input
    if not isinstance(document, dict):
        raise ValueError("The document must be a dictionary.")
    
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Ensure MongoDB is running locally
    db = client[db_name]  # Access the specified database
    collection = db[collection_name]  # Access the specified collection

    # Insert the document
    result = collection.insert_one(document)

    # Return the inserted document's unique identifier (_id) as a string
    return str(result.inserted_id)
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