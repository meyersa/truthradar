import unittest
from lib.types import Result
from lib.chatgpt import fill_gpt, verify_title, verify_reason, verify_score, query

class TestChatGPT(unittest.TestCase):
    def test_fill_gpt(self):
        """
        Test fill_gpt
        """
        res = Result(id="test123", content="The sky is blue.", predictions=[], input="Testing")
        result = fill_gpt(res)

        self.assertIsNotNone(result)
        self.assertIsInstance(result.title, str)
        self.assertTrue(5 <= len(result.title) <= 50)
        self.assertIsInstance(result.reason, str)
        self.assertTrue(0 < len(result.reason) <= 750)
        self.assertEqual(len(result.predictions), 1)
        self.assertIsInstance(result.predictions[0]["score"], float)
        self.assertGreaterEqual(result.predictions[0]["score"], 0.0)
        self.assertLessEqual(result.predictions[0]["score"], 1.0)

    def test_query(self):
        """
        Test query directly with real content.
        """
        score, reason, title = query("The earth orbits the sun.")

        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

        self.assertIsInstance(reason, str)
        self.assertTrue(0 < len(reason) <= 750)

        self.assertIsInstance(title, str)
        self.assertTrue(5 <= len(title) <= 50)

    def test_verify_score(self):
        """
        Test verify_score function.
        """
        self.assertTrue(verify_score(0.0))
        self.assertTrue(verify_score(0.5))
        self.assertTrue(verify_score(1.0))
        self.assertFalse(verify_score(-0.1))
        self.assertFalse(verify_score(1.1))
        self.assertFalse(verify_score("bad"))

    def test_verify_reason(self):
        """
        Test verify_reason function.
        """
        self.assertTrue(verify_reason("This is a valid reason."))
        self.assertFalse(verify_reason(""))
        self.assertFalse(verify_reason(12345))
        self.assertFalse(verify_reason("a" * 1001))

    def test_verify_title(self):
        """
        Test verify_title function.
        """
        self.assertTrue(verify_title("Short Title"))
        self.assertTrue(verify_title("A" * 50))
        self.assertFalse(verify_title(""))
        self.assertFalse(verify_title("abcd"))
        self.assertFalse(verify_title("A" * 51))
        self.assertFalse(verify_title(12345))

if __name__ == "__main__":
    unittest.main()
