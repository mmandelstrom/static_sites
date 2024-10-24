import unittest

from markdown_blocks import *

class TestHTMLNode(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown_text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertEqual(markdown_to_blocks(markdown_text), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ])

    def test_markdown_to_blocks_just_list(self):
        markdown_text = """
* This is the start of a list
* Second item of list
* Third list item
* Fourth
"""
        self.assertEqual(markdown_to_blocks(markdown_text), [
            "* This is the start of a list\n* Second item of list\n* Third list item\n* Fourth"
        ])

    def test_markdown_to_blocks_list_with_extra_line(self):
        markdown_text = """
* First list item
* Second

* third
* fourth
"""
        self.assertEqual(markdown_to_blocks(markdown_text), [
            "* First list item\n* Second",
            "* third\n* fourth"
        ])


if __name__ == "__main__":
    unittest.main()