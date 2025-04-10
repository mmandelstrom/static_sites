import unittest

from textnode import TextNode, TextType
from node_conversion import text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode, HTMLNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a textnode", TextType.ITALIC, "https://url.se")
        self.assertEqual(node, TextNode("This is a textnode", TextType.ITALIC, "https://url.se"))


    def test_none_url(self):
        node = TextNode("This is a textnode", TextType.TEXT, None)
        self.assertEqual(node, TextNode("This is a textnode", TextType.TEXT))

    def test_not_equal_text_type(self):
        node = TextNode("This is a textnode", TextType.BOLD)
        node2 = TextNode("This is a textnode", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a textnode", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode("This is a textnode", TextType.CODE, "https://url.se")
        node2 = TextNode("This is a textnode", TextType.CODE, "https:/url.se")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a textnode", TextType.BOLD, "https://boot.dev")
        self.assertEqual('TextNode(This is a textnode, bold, https://boot.dev)', node.__repr__())

    def test_text_node_to_html_text(self):
        node = text_node_to_html_node(TextNode("This is a textnode", TextType.TEXT))
        self.assertEqual(node, LeafNode(None, "This is a textnode"))

    def test_text_node_to_html_bold(self):
        node = text_node_to_html_node(TextNode("This is a textnode", TextType.BOLD))
        self.assertEqual(node, LeafNode("b", "This is a textnode"))

    def test_text_node_to_html_italic(self):
        node = text_node_to_html_node(TextNode("This is a textnode", TextType.ITALIC))
        self.assertEqual(node, LeafNode("i", "This is a textnode"))

    def test_text_node_to_html_code(self):
        node = text_node_to_html_node(TextNode("This is a textnode", TextType.CODE))
        self.assertEqual(node, LeafNode("code", "This is a textnode"))

    def test_text_node_to_html_link(self):
        node = text_node_to_html_node(TextNode("click me!", TextType.LINK, "https://boot.dev"))
        self.assertEqual(node, LeafNode("a", "click me!", {'href': "https://boot.dev"}))

    def test_text_node_to_html_image(self):
        node = text_node_to_html_node(TextNode("beautiful image", TextType.IMAGE, "https://my_image.com"))
        self.assertEqual(node, LeafNode("img", "", {'src': 'https://my_image.com', 'alt': 'beautiful image'}))

    def test_test_node_to_html_invalid(self):
        node = TextNode("div", 999)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Invalid Text type")

    def test_test_node_to_html_image_no_url(self):
        node = TextNode("beautiful image", TextType.IMAGE, "")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), f"Image nodes require a non-empty 'url'. Got: {node.url}")

    def test_test_node_to_html_link_no_url(self):
        node = TextNode("click me!", TextType.LINK, "")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), f"Link nodes require a non-empty 'url'. Got: {node.url}")

    def test_test_node_to_html_image_none_url(self):
        node = TextNode("beautiful image", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), f"Image nodes require a non-empty 'url'. Got: {node.url}")

    def test_test_node_to_html_link_none_url(self):
        node = TextNode("click me!", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), f"Link nodes require a non-empty 'url'. Got: {node.url}")

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

if __name__ == "__main__":
    unittest.main()
