import unittest
from pymongo import MongoClient
def find_mongo_document_by_uuid(uuid_value, db_name="test_database", collection_name="test_collection"):
    """
    Finds a MongoDB document in the specified database and collection by UUID.

    Args:
        uuid_value (str): The UUID value to search for.
        db_name (str, optional): The name of the database. Defaults to "test_database".
        collection_name (str, optional): The name of the collection. Defaults to "test_collection".

    Returns:
        dict: The document matching the UUID, or None if no document is found.

    Raises:
        ValueError: If the UUID value is not a string.
        Exception: If the MongoDB query fails for any reason.
    """
    # Validate the input
    if not isinstance(uuid_value, str):
        raise ValueError("The UUID value must be a string.")
    
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Ensure MongoDB is running locally
    db = client[db_name]  # Access the specified database
    collection = db[collection_name]  # Access the specified collection

    # Find the document by UUID
    document = collection.find_one({"UUID": uuid_value})
    
    return document
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
