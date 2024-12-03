import unittest
from pymongo import MongoClient
def update_field_by_uuid(uuid_value, field_name, new_value, db_name="test_database", collection_name="test_collection"):
    # Validate inputs
    if not isinstance(uuid_value, str):
        raise ValueError("The UUID value must be a string.")
    if not isinstance(field_name, str):
        raise ValueError("The field name must be a string.")
    
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Ensure MongoDB is running locally
    db = client[db_name]  # Access the specified database
    collection = db[collection_name]  # Access the specified collection

    # Update the document
    result = collection.find_one_and_update(
        {"UUID": uuid_value},                # Query to find the document by UUID
        {"$set": {field_name: new_value}},   # Update operation to set the new value
        return_document=True                 # Return the updated document
    )

    return result
class TestUpdateFieldByUUID(unittest.TestCase):
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

    def test_update_field(self):
        # Update the email field
        new_email = "updated.email@example.com"
        updated_document = update_field_by_uuid(self.test_uuid, "email", new_email)

        # Verify the update
        self.assertIsNotNone(updated_document)
        self.assertEqual(updated_document["email"], new_email)

    def test_update_field_document_not_found(self):
        # Test with a non-existent UUID
        result = update_field_by_uuid("non-existent-uuid", "email", "new@example.com")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
