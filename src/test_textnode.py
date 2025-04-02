import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()