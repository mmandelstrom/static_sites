import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()