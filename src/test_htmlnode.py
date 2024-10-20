import unittest

from textnode import *
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

#Testing the text_to_html_node function with all text_types

    def test_text_to_html_node_bold(self):
        node = TextNode('This is my text', TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node), LeafNode('b', 'This is my text'))

    def test_text_to_html_node_italic(self):
        node = TextNode('This is my text', TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node), LeafNode('i', 'This is my text'))

    def test_text_to_html_node_code(self):
        node = TextNode('This is my text', TextType.CODE)
        self.assertEqual(text_node_to_html_node(node), LeafNode('code', 'This is my text'))

    def test_text_to_html_node_link(self):
        node = TextNode('This is my text', TextType.LINK, "https://boot.dev")
        self.assertEqual(text_node_to_html_node(node), LeafNode('a', 'This is my text', "https://boot.dev"))

    def test_text_to_html_node_text(self):
        node = TextNode('This is my text', TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node), LeafNode(value = 'This is my text'))

    def test_text_to_html_node_value_error(self):
        with self.assertRaises(ValueError):
            node = text_node_to_html_node(TextNode('This is my text', 'asdasd'))

    def test_text_to_html_node_attribute_error(self):
        with self.assertRaises(AttributeError):
            node = text_node_to_html_node(TextNode('This is my text', TextType.ASD))
    

#Testing text_to_html function chained with to_html method

    def test_text_to_html_node_code_link_to_html(self):
        node = TextNode('This is my text', TextType.LINK, {"href": "https://boot.dev"})
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="https://boot.dev">This is my text</a>')


    def test_text_to_html_node_code_bold_to_html(self):
        node = TextNode('This is my text', TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), '<b>This is my text</b>')


    def test_text_to_html_node_code_italic_to_html(self):
        node = TextNode('This is my text', TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(), '<i>This is my text</i>')


    def test_text_to_html_node_code_code_to_html(self):
        node = TextNode('This is my text', TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(), '<code>This is my text</code>')  

    def test_text_to_html_node_code_text_to_html(self):
        node = TextNode('This is my text', TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(), 'This is my text')


    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )





if __name__ == "__main__":
    unittest.main()