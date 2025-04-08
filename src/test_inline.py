import unittest
from inline_funcs import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

class TestInline(unittest.TestCase):

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is some text with a **bold** word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is some text with a _italic_ word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is some text with a `code` word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ])

    def test_split_nodes_delimiter_multiple_bold(self):
        node = TextNode("This is some text with a **bold** word and **another** word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
            ])

    def test_split_nodes_delimiter_multiple_italic(self):
        node = TextNode("This is some text with a _italic_ word and _italic_ word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
            ])

    def test_split_nodes_delimiter_multiple_code(self):
        node = TextNode("This is some text with a `code` word and `code` word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_no_closing_bold(self):
        node = TextNode("This is some text with a **bold* word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), f"No closing delimiter found for **")

    def test_split_nodes_delimiter_no_closing_italic(self):
        node = TextNode("This is some text with a _italic word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(str(context.exception), f"No closing delimiter found for _")

    def test_split_nodes_delimiter_no_closing_code(self):
        node = TextNode("This is some text with a `code word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), f"No closing delimiter found for `")

    def test_split_nodes_delimiter_invalid_delimiter(self):
        node = TextNode("This is some text with *invalid* delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(str(context.exception), f"* is not a valid markdown delimiter")

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("This is some text with a `code word`", TextType.TEXT),
            TextNode("This is the second with `code`", TextType.TEXT),
            TextNode("`code` words etc", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("code word", TextType.CODE),
            TextNode("This is the second with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("code", TextType.CODE),
            TextNode(" words etc", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_start_and_end(self):
        node = TextNode("**bold** word in the start and **end**", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("bold", TextType.BOLD),
            TextNode(" word in the start and ", TextType.TEXT),
            TextNode("end", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_start_italic(self):
        node = TextNode("_italic words_ in the beginning", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
            TextNode("italic words", TextType.ITALIC),
            TextNode(" in the beginning", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_end_code(self):
        node = TextNode("sentence ending with `code`", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
            TextNode("sentence ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ])

    def test_split_nodes_delimiter_no_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_text_type_image(self):
        node = TextNode("image of fun stuff", TextType.IMAGE, "https://image.com")
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.IMAGE), [
            TextNode("image of fun stuff", TextType.IMAGE, "https://image.com")
        ])

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
        "This is text with an [to boot dev](https://www.boot.dev))"
    )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is some text with ![image](image.com) and some more text with ![img](img.img) and so on"
        )
        self.assertListEqual([("image", "image.com"), ("img", "img.img")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is a link [google](google.com) and some text [boot dev](boot.dev) and text"
        )
        self.assertListEqual([("google", "google.com"), ("boot dev", "boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()
