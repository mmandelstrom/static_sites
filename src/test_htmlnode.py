import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "This is a node", None, {
            "href": "https://www.google.com",
            "target": "_blank",})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_props_exception(self):
        node = HTMLNode("p", "This is a node")
        with self.assertRaises(Exception) as context:
            node.props_to_html()
        self.assertEqual(str(context.exception), "HTMLNode does not contains any props")

    def test_default_values(self):
        node = HTMLNode()
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node.__repr__(), node2.__repr__())

    def test_repr_tag_value(self):
        node = HTMLNode("p", "value")
        self.assertEqual("HTMLNode(p, value, None, None)", node.__repr__())

    def test_repr_all(self):
        node = HTMLNode("a", "this is a value", "child", {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual("HTMLNode(a, this is a value, child, {'href': 'https://www.google.com', 'target': '_blank'})", node.__repr__())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', node.to_html())

    def test_leaf_to_html_a_2(self):
        node = LeafNode("a", "Click me!", {'href': 'https://www.google.com', 'target': '_blank'})
        self.assertEqual('<a href="https://www.google.com" target="_blank">Click me!</a>', node.to_html())

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "this is the code value")
        self.assertEqual('<code>this is the code value</code>', node.to_html())

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is the value")
        self.assertEqual("This is the value", node.to_html())


if __name__ == "__main__":
    unittest.main()