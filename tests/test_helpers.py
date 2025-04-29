import unittest
from lib.helpers import save_result, get_result, get_recent, hash_text, results_collection
from lib.types import Result

class TestDBIntegration(unittest.TestCase):
    """
    MongoDB integration tests without clearing the database.
    """

    def setUp(self):
        self.sample_text = "The sky is pink today."
        self.sample_id = hash_text(self.sample_text)
        self.sample_result = Result(
            id=self.sample_id,
            input=self.sample_text,
            content="Test Content",
            predictions={"test": "value"}
        )

    def test_save_get_recent_delete(self):
        # Save result
        saved = save_result(self.sample_result)
        self.assertTrue(saved, "Result should be saved successfully")

        # Fetch result by ID
        fetched = get_result(self.sample_id)
        self.assertIsNotNone(fetched, "Fetched result should not be None")
        self.assertEqual(fetched.id, self.sample_id, "Fetched ID should match saved ID")

        # Fetch recent results
        recent = get_recent(10)  # Assume 10 is enough to include the new one
        self.assertIsInstance(recent, list, "Recent should return a list")
        self.assertTrue(any(r.id == self.sample_id for r in recent), "Saved result should appear in recent")

        # Delete the result
        delete_result = results_collection.delete_one({"id": self.sample_id})
        self.assertEqual(delete_result.deleted_count, 1, "Result should be deleted successfully")

        # Ensure it no longer exists
        fetched_after_delete = get_result(self.sample_id)
        self.assertIsNone(fetched_after_delete, "Deleted result should no longer be found")

