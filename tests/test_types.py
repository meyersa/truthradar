from lib.types import Result
import unittest

class TestResult(unittest.TestCase): 
    def test_class_init(self): 
        res = Result(id="12345", input="Testing")

        self.assertIsNotNone(res.id)
        self.assertIsNotNone(res.input)
        self.assertIsNotNone(res.timestamp)

        self.assertIsNone(res.link)
        self.assertIsNone(res.content)
        self.assertIsNone(res.title)
        self.assertIsNone(res.result)
        self.assertIsNone(res.reason)


