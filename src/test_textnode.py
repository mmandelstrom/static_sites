import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_url_not_node(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
        self.assertIsNotNone(node.url)
        
    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def text_not_eq(self):
        node = TextNode("This is not a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def invalid_texttype(self):
        with self.assertRaises(AttributeError):
            node = TextNode("This is a text node", TextType.asdasdsa, "https://boot.dev")

    def test_all_text_types(self):
        try:
            node = TextNode("This is a text node", TextType.TEXT)
            node2 = TextNode("This is a text node", TextType.BOLD)
            node3 = TextNode("This is a text node", TextType.ITALIC)
            node4 = TextNode("This is a text node", TextType.CODE)
            node5 = TextNode("This is a text node", TextType.LINK)
            node6 = TextNode("This is a text node", TextType.IMAGE)

        except Exception as e:
            self.fail(f"TextNode creation failed with a valid TextType: {e}")


if __name__ == "__main__":
    unittest.main()