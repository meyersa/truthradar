from lib.parsing import clean_input, is_url, parse_site, get_input
import unittest


class TestCleanInput(unittest.TestCase):
    def test_normal_input(self):
        content = ' Hello <world>! This is some test input. '
        result = clean_input(content)
        self.assertEqual(result, 'Hello ltworldgt This is some test input.')

    def test_long_input(self):
        content = 'a' * 1500
        result = clean_input(content)
        self.assertEqual(result, 'a' * 1000)

    def test_special_characters(self):
        content = 'Hello! This $tring has special characters @#!%'
        result = clean_input(content)
        self.assertEqual(result, 'Hello This tring has special characters ')

    def test_none_input(self):
        result = clean_input(None)
        self.assertIsNone(result)


class TestIsUrl(unittest.TestCase):
    def test_link_input(self):
        g_url = "https://google.com"
        self.assertTrue(is_url(g_url))

        gh_url = "https://github.com/meyersa/tornado_helper/blob/main/tests/test_goes.py"
        self.assertTrue(is_url(gh_url))

        yt_url = "https://www.youtube.com/watch?v=0kQXOTcEB_E"
        self.assertTrue(is_url(yt_url))

    def test_content_input(self):
        c1 = "This is a test"
        self.assertFalse(is_url(c1))

        c2 = "Non cupidatat laboris veniam ut."
        self.assertFalse(is_url(c2))

        c3 = "Nisi duis nulla Lorem duis ad et cupidatat excepteur cillum quis aute quis labore eu. Incididunt nulla minim ipsum magna reprehenderit proident labore. Eu et incididunt id in anim quis consectetur duis nulla quis est. Dolore esse voluptate officia in commodo deserunt elit consectetur culpa anim laborum. Magna voluptate nostrud veniam ipsum."
        self.assertFalse(is_url(c3))

    def test_bad_input(self):
        b1 = ""
        self.assertFalse(is_url(b1))

        b2 = "this/that"
        self.assertFalse(is_url(b2))

        b3 = "google.com"
        self.assertFalse(is_url(b3))


class TestParseSite(unittest.TestCase):
    def test_link_input(self):
        self.assertIsNotNone(parse_site("https://google.com"))


class TestGetInput(unittest.TestCase):
    def test_normal_input(self):
        content = ' Hello <world>! '
        result = get_input(content)
        self.assertEqual(result, 'Hello ltworldgt')

    def test_non_url_text(self):
        content = 'This is just normal text input'
        result = get_input(content)
        self.assertEqual(result, 'This is just normal text input')

    def test_url_input(self):
        url = "https://www.example.com"
        result = get_input(url)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_empty_input(self):
        result = get_input("")
        self.assertIsNone(result)

    def test_none_input(self):
        result = get_input(None)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
