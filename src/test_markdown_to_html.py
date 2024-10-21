import unittest

from textnode import *
from htmlnode import *
from markdown_to_html import *

class TestHTMLNode(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode('This is the value **with bold** inside of it', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode('This is the value ', TextType.TEXT), TextNode('with bold', TextType.BOLD), TextNode(' inside of it', TextType.TEXT)])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode('This is the value *with italic* inside of it', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), [TextNode('This is the value ', TextType.TEXT), TextNode('with italic', TextType.ITALIC), TextNode(' inside of it', TextType.TEXT)])

    def test_split_nodes_delimiter_code(self):
        node = TextNode('This is the value `code` inside of it', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [TextNode('This is the value ', TextType.TEXT), TextNode('code', TextType.CODE), TextNode(' inside of it', TextType.TEXT)])

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode('This first node **with a bold sentence**', TextType.TEXT),
            TextNode('This is the second node *with italic sentence* inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
        ]
        with_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        with_italic = split_nodes_delimiter(with_bold, "*", TextType.ITALIC)
        with_code = split_nodes_delimiter(with_italic, "`", TextType.CODE)
        self.assertEqual(with_bold, [
            TextNode('This first node ', TextType.TEXT),
            TextNode('with a bold sentence', TextType.BOLD),
            TextNode('This is the second node *with italic sentence* inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
            ])

    def test_split_nodes_no_end_delimiter(self):
        node = [TextNode('this is the text **without ending delimiter*', TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "**", TextType.BOLD)

    def test_split_nodes_no_delimiter(self):
        node = [TextNode('this is the text without delimiter', TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), [TextNode('this is the text without delimiter', TextType.TEXT)])

    def test_split_nodes_nested_no_delimiter(self):
        nodes = [
            TextNode('This first node **with a bold sentence**', TextType.TEXT),
            TextNode('This is the second node with a normal sentence inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
        ]
        with_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        with_italic = split_nodes_delimiter(with_bold, "*", TextType.ITALIC)
        with_code = split_nodes_delimiter(with_italic, "`", TextType.CODE)
        self.assertEqual(with_bold, [
            TextNode('This first node ', TextType.TEXT),
            TextNode('with a bold sentence', TextType.BOLD),
            TextNode('This is the second node with a normal sentence inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
            ])

    def test_split_nodes_start_with_delimiter(self):
        node = TextNode('**with bold** text after', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode('with bold', TextType.BOLD), TextNode(' text after', TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()