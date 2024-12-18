import unittest
import os
from sqlalchemy.orm import declarative_base, clear_mappers
from sqlalchemy import MetaData
from json_to_sqlalchemy import load_json_to_models

class TestJSONToSQLAlchemy(unittest.TestCase):
    def setUp(self):
        """
        Set up the DSL JSON for testing and clear existing metadata.
        """
        clear_mappers()  # Reset SQLAlchemy mappers
        self.Base = declarative_base(metadata=MetaData())  # Create a new Base with fresh MetaData
        # Use path relative to the test file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.dsl_json = os.path.join(current_dir, "shipping_converted.json")
        self.models = load_json_to_models(self.dsl_json, self.Base)

    def test_model_creation(self):
        """
        Test that models are dynamically created and have correct attributes.
        """
        manifest = self.models.get("S001_Manifest")
        self.assertIsNotNone(manifest, "Model S001_Manifest was not created.")

        # Check attributes
        columns = {c.name for c in manifest.__table__.columns}
        expected_columns = {"id", "bill_of_lading", "shipper_id", "consignee_id"}
        self.assertTrue(expected_columns.issubset(columns), "Expected columns not found in S001_Manifest.")

    def test_foreign_keys(self):
        """
        Test that foreign keys are correctly applied.
        """
        manifest = self.models.get("S001_Manifest")
        self.assertIsNotNone(manifest, "Model S001_Manifest was not created.")

        # Validate foreign keys
        foreign_keys = {fk.target_fullname for fk in manifest.__table__.foreign_keys}
        expected_foreign_keys = {"S015_Client.id", "S015_Client.id"}
        self.assertTrue(expected_foreign_keys.issubset(foreign_keys), "Foreign keys not correctly set.")

    def test_primary_keys(self):
        """
        Test that primary keys are correctly assigned.
        """
        manifest = self.models.get("S001_Manifest")
        self.assertIsNotNone(manifest, "Model S001_Manifest was not created.")

        # Check primary key constraints
        primary_keys = {pk.name for pk in manifest.__table__.primary_key}
        self.assertTrue(primary_keys, f"Table 'S001_Manifest' has no primary key.")
        self.assertIn("id", primary_keys, "Primary key 'id' is missing in S001_Manifest.")


if __name__ == "__main__":
    unittest.main()
