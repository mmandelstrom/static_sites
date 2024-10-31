import unittest

from generate_page import extract_title

class TestHTMLNode(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# This has a header\n and some other text"
        self.assertEqual(extract_title(markdown), "This has a header")

    def test_extract_title_exception(self):
        markdown = "## Incorrcet header"
        with self.assertRaises(Exception):
            extract_title(markdown)


    def test_extract_title_exception_2(self):
        markdown = "missing header"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()