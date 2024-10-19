import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "This is the child value", {"href": "https://www.google.com"})])
        with self.assertRaises(ValueError):
            node.to_html()

        
    def test_to_html_no_child(self):
        node = ParentNode("div", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()

    
    def test_to_html_one_child_with_prop(self):
        node = ParentNode("div", [LeafNode("i", "this is a single child", {"href": "https://www.google.com"})])
        self.assertEqual(node.to_html(), '<div><i href="https://www.google.com">this is a single child</i></div>')

    def test_parent_prop_no_child_prop(self):
        node = ParentNode("a", [LeafNode("p", "Single child")], {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com"><p>Single child</p></a>')

    def test_parent_prop_multiple_children_no_prop(self):
        node = ParentNode("a", [LeafNode('p', 'This is the first child'), LeafNode('b', 'This is the second child'), LeafNode('i', 'This is the third child')], {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev"><p>This is the first child</p><b>This is the second child</b><i>This is the third child</i></a>')


    def test_parent_prop_mutliple_children_prop(self):
        node = ParentNode(
            "a", 
            [
                LeafNode('a', 'This is the first child', {"href": "https://boot.dev"}),
                LeafNode('i', 'This is the second child', {"href": "https://google.se"}),
                LeafNode('b', 'This is the third child', {"href": "https://youtube.com"})], 
                {"href": "https://asd.se"}
                )
        self.assertEqual(node.to_html(), '<a href="https://asd.se"><a href="https://boot.dev">This is the first child</a><i href="https://google.se">This is the second child</i><b href="https://youtube.com">This is the third child</b></a>')


    def test_parent_no_prop_multiple_children_prop(self):
        node = ParentNode(
            "div", 
            [
                LeafNode('a', 'This is the first child', {"href": "https://boot.dev"}),
                LeafNode('i', 'This is the second child', {"href": "https://google.se"}),
                LeafNode('b', 'This is the third child', {"href": "https://youtube.com"})]
                )
        self.assertEqual(node.to_html(), '<div><a href="https://boot.dev">This is the first child</a><i href="https://google.se">This is the second child</i><b href="https://youtube.com">This is the third child</b></div>')

    def test_parent_no_prop_multiple_children(self):
        node = ParentNode(
            "div", 
            [
                LeafNode('a', 'This is the first child', {"href": "https://boot.dev"}),
                LeafNode('i', 'This is the second child'),
                LeafNode('b', 'This is the third child', {"href": "https://youtube.com"})]
                )
        self.assertEqual(node.to_html(), '<div><a href="https://boot.dev">This is the first child</a><i>This is the second child</i><b href="https://youtube.com">This is the third child</b></div>')


    def test_nested_parentnode(self):
        node = ParentNode(
            "div",
            [
                ParentNode('div', [
                    LeafNode('p', "First nested leaf"),
                    LeafNode('i', 'Second nested leaf')
                ])
            ]
        )
        self.assertEqual(node.to_html(), '<div><div><p>First nested leaf</p><i>Second nested leaf</i></div></div>')

    def test_parent_nested_in_parent(self):
        self.maxDiff = None
        node = ParentNode(
            "div",
            [
                LeafNode('p', 'First leaf', {"href": "https://boot.dev"}),
                ParentNode('div', [
                    LeafNode('i', 'Nested leaf', {"href": "https://google.se"}),
                    ParentNode('div', [
                        LeafNode('p', 'third level leaf')
                    ], {"href": "https://youtube.com"}),
                    ParentNode('div', [
                        LeafNode('b', 'fourth level leaf'),
                        LeafNode('p', 'fourth level leaf 2')
                    ])
                ])
            ]
        )
        self.assertEqual(node.to_html(), '<div><p href="https://boot.dev">First leaf</p><div><i href="https://google.se">Nested leaf</i><div href="https://youtube.com"><p>third level leaf</p></div><div><b>fourth level leaf</b><p>fourth level leaf 2</p></div></div></div>')
                         
    def test_nested_parent_with_empty_child_list(self):
        node = ParentNode(
            "div", [
                ParentNode('p', []),
                LeafNode('p', 'leaf')
            ]
        )
        
        with self.assertRaises(ValueError):
            node.to_html()

    def test_nested_parent_with_none_child(self):
        node = ParentNode(
            "div", [
                ParentNode('p', None),
                LeafNode('p', 'leaf')
            ]
        )
        
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()