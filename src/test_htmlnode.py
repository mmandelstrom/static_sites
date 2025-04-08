import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
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

    def test_parent_to_html_div_1_child(self):
        node = ParentNode("div", [
            LeafNode("p", "Child 1 value")
        ])
        self.assertEqual(node.to_html(), "<div><p>Child 1 value</p></div>")

    def test_parent_to_html_anchor_multiple_children(self):
        node = ParentNode("a", [
            LeafNode("p", "child 1 value"),
            LeafNode("a", "click me!", {'href': 'https://www.google.com', 'target': '_blank'}),
            LeafNode(None, "text with no tag"),
            LeafNode("img", "image", {'href': 'https://www.myimage.com', 'target': '_blank'})
        ], {'href': 'https://boot.dev'})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev"><p>child 1 value</p><a href="https://www.google.com" target="_blank">click me!</a>text with no tag<img href="https://www.myimage.com" target="_blank">image</img></a>')

    def test_nested_parent_and_leaf(self):
        node = ParentNode("div", [
            LeafNode("p", "first child"),
            ParentNode("div", [
                LeafNode("code", "first nested child"),
                ParentNode("div", [
                    LeafNode("p", "second level nest")
                ])
            ]),
            LeafNode("a", "second child", {'href': 'https://boot.dev'})
        ])
        self.assertEqual(node.to_html(), '<div><p>first child</p><div><code>first nested child</code><div><p>second level nest</p></div></div><a href="https://boot.dev">second child</a></div>')

    def test_parentnode_value_error_tag(self):
        node = ParentNode(None,[
            LeafNode("p", "first child")
        ])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Parentnode must have a tag")

    def test_parentnode_value_error_child(self):
        node = ParentNode("div",[])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_parentnode_value_error_child_2(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")

    


if __name__ == "__main__":
    unittest.main()