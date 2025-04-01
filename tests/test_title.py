from lib.title import download, summarize, get_title
from lib.types import Result
import unittest

class TestDownload(unittest.TestCase): 
    def test_link(self): 
        res = download("https://google.com")

        self.assertIsNotNone(res)
        self.assertGreater(len(res), 5)

class TestSummarize(unittest.TestCase): 
    def test_summarize(self): 
        content = "This is a text about summarization, your goal is to mention that. Please note that summarization helps because when a link can't be located, this is how we will infer context."
        res = summarize(content)

        self.assertIsNotNone(res)
        self.assertGreater(len(res), 4)
        self.assertLess(len(res), 50)

class TestGetTitle(unittest.TestCase): 
    def test_link(self): 
        link_res = Result(12345, "This is something with links")
        link_res.link = "https://google.com"

        res = get_title(link_res)

        self.assertIsNotNone(res.title)
        self.assertGreater(len(res.title), 4)
        self.assertLess(len(res.title), 50)

        test_res = download(link_res.link)
        self.assertEqual(res.title, test_res)

    def test_summarize(self): 
        sum_res = Result(12345, "This is something with links")

        res = get_title(sum_res)

        self.assertIsNotNone(res.title)
        self.assertGreater(len(res.title), 4)
        self.assertLess(len(res.title), 50)
  