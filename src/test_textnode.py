import unittest

from textnode import TextNode, TextType
from node_conversion import text_node_to_html_node
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


if __name__ == "__main__":
    unittest.main()
