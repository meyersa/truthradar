from lib.types import Result
from lib.model import verify_reason, verify_result, query, test
import unittest

class TestVerifyReason(unittest.TestCase): 
    def test_too_long(self): 
        self.assertFalse(verify_reason("A"*1001))

    def test_not_str(self): 
        self.assertFalse(verify_reason(5))

    def test_good(self): 
        self.assertTrue(verify_reason("This is good"))

class TestVerifyResult(unittest.TestCase): 
    def test_too_high(self): 
        self.assertFalse(verify_result(101))

    def test_too_low(self): 
        self.assertFalse(verify_result(-1))

    def test_good(self): 
        self.assertTrue(verify_result(50))

class TestQuery(unittest.TestCase): 
    def test_query(self): 
        content = "Ronald Reagon was born in 2004"
        res = query(content)

        # Should be closer to 100 (very fake)
        self.assertGreater(res[0], 75)
        self.assertGreater(len(res[1]), 100)

class TestTest(unittest.TestCase): 
    def test_full(self): 
        in_res = Result(id=12345, input="", content="Joe Biden was the first female president")
        res = test(in_res)

        self.assertGreater(res.result, 75)
        self.assertGreater(len(res.reason), 100)
