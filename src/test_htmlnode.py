import unittest

from htmlnode import HTMLNode, LeafNode


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


    def test_leaf_to_html_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()
    

if __name__ == "__main__":
    unittest.main()