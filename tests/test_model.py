import unittest
from lib.model import predict
from lib.types import Result

class TestModel(unittest.TestCase):
    """
    Unit tests for the predict function.
    """

    def setUp(self):
        """
        Create a sample Result object for testing.
        """
        self.sample_result = Result(
            id="test123",
            content="The sky is green today.",
            predictions=[],
            input="Testing"
        )

    def test_successful_prediction(self):
        """
        Tests that a successful API call correctly updates Result.predictions.
        """
        updated_result = predict(self.sample_result)

        self.assertIsNotNone(updated_result, "Predict should not return None on success.")
        self.assertIsNotNone(updated_result.predictions, "Predictions field should be populated.")
        self.assertIsInstance(updated_result.predictions, list, "Predictions should be a list.")

        for pred in updated_result.predictions:
            self.assertIn('name', pred)
            self.assertIn('score', pred)
            self.assertIn('duration_ms', pred)
            self.assertIsInstance(pred['name'], str)
            self.assertIsInstance(pred['score'], float)
            self.assertIsInstance(pred['duration_ms'], float)

if __name__ == "__main__":
    unittest.main()
