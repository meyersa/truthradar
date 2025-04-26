import unittest
from unittest.mock import patch, Mock
from lib.model import predict  # replace with actual filename
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
            predictions=None,
            input="Testing"
        )

    @patch('requests.post')  # replace with your actual module path
    def test_successful_prediction(self, mock_post):
        """
        Tests that a successful API call correctly updates Result.predictions.
        """

        # Mocked API response content
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'predictions': [
                {'name': 'LogisticRegression', 'score': 0.660553220029004, 'duration_ms': 0.46},
                {'name': 'BernoulliNB', 'score': 0.9004633486166935, 'duration_ms': 3.41},
                {'name': 'XGBoost', 'score': 0.7203407287597656, 'duration_ms': 1.77}
            ],
            'duration_ms': 4.77
        }
        mock_post.return_value = mock_response

        # Call the function
        updated_result = predict(self.sample_result)

        # Assertions
        self.assertIsNotNone(updated_result, "Predict should not return None on success.")
        self.assertIsNotNone(updated_result.predictions, "Predictions field should be populated.")
        self.assertIsInstance(updated_result.predictions, dict, "Predictions should be a dictionary.")
        self.assertIn('predictions', updated_result.predictions, "Response should contain 'predictions' key.")

        preds = updated_result.predictions['predictions']
        self.assertIsInstance(preds, list, "Predictions['predictions'] should be a list.")
        self.assertGreater(len(preds), 0, "Predictions list should not be empty.")

        for pred in preds:
            self.assertIn('name', pred)
            self.assertIn('score', pred)
            self.assertIn('duration_ms', pred)
            self.assertIsInstance(pred['name'], str)
            self.assertIsInstance(pred['score'], float)
            self.assertIsInstance(pred['duration_ms'], float)

if __name__ == "__main__":
    unittest.main()
