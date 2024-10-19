import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode("p", "This is my value", None, {
    "href": "https://www.google.com", 
    "target": "_blank",
})

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_none_prop_to_html(self):
        node = HTMLNode("div", "This is a value")
        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        node = HTMLNode("p", "This is my value", None, {
    "href": "https://www.google.com", 
    "target": "_blank",
})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("div", "This is my value")
        self.assertEqual(node.__repr__(), "HTMLNode(Tag = div, Value = This is my value, Children = None, Props = None)")

if __name__ == "__main__":
    unittest.main()