import unittest

from markdown_blocks import *

class TestHTMLNode(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown_text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertEqual(markdown_to_blocks(markdown_text), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ])

    def test_markdown_to_blocks_just_list(self):
        markdown_text = """
* This is the start of a list
* Second item of list
* Third list item
* Fourth
"""
        self.assertEqual(markdown_to_blocks(markdown_text), [
            "* This is the start of a list\n* Second item of list\n* Third list item\n* Fourth"
        ])

    def test_markdown_to_blocks_list_with_extra_line(self):
        markdown_text = """
* First list item
* Second

* third
* fourth
"""
        self.assertEqual(markdown_to_blocks(markdown_text), [
            "* First list item\n* Second",
            "* third\n* fourth"
        ])


    def test_block_to_block_type_unordered_list(self):
        block = "* This is the first list item\n* This is the second\n* And the third"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_heading_1(self):
        block = "# This is a heading 1"
        self.assertEqual(block_to_block_type(block), "heading_1")

    def test_block_to_block_type_heading_2(self):
        block = "## This is a heading 2"
        self.assertEqual(block_to_block_type(block), "heading_2")

    def test_block_to_block_type_heading_3(self):
        block = "### This is a heading 2"
        self.assertEqual(block_to_block_type(block), "heading_3")

    def test_block_to_block_type_heading_4(self):
        block = "#### This is a heading 2"
        self.assertEqual(block_to_block_type(block), "heading_4")

    def test_block_to_block_type_heading_5(self):
        block = "##### This is a heading 2"
        self.assertEqual(block_to_block_type(block), "heading_5")

    def test_block_to_block_type_heading_6(self):
        block = "###### This is a heading 2"
        self.assertEqual(block_to_block_type(block), "heading_6")

    def test_block_to_block_type_invalid_heading(self):
        block = "#This is just a paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_code(self):
        block = "```this is a code block !##!```"
        self.assertEqual(block_to_block_type(block), "code_block")

    def test_block_to_block_type_invalid_code(self):
        block = "```this is a code block !##!``"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_single_line_quote(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_multi_line_quote(self):
        block = ">This is a quote\n>So is this\n> And also this"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_to_block_type_invalid_multi_line_quote(self):
        block = ">This is a quote\n>So is this\n And also this"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_single_line_ul(self):
        block = "* List"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_multi_line_ul(self):
        block = "* List item 1\n- List item 2\n* List item 3"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_invalid_multi_line_ul(self):
        block = "* List item 1\n- List item 2\n*List item 3"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_single_line_ol(self):
        block = "1. my list"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_block_type_multi_line_ol(self):
        block = "1. my list\n2. second line\n3. third\n4. fourth"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_block_type_invalid_multi_line_ol(self):
        block = "1. my list\n2. second line\n3. third\n5. fourth"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_markdown_to_html_code_block(self):
       markdown = "```this is some*itlaic* **bold** code And some more stuff```"
       self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [HTMLNode("pre", None, HTMLNode("code", None, LeafNode(None, "this is some*itlaic* **bold** code And some more stuff")))]))

    def test_markdown_to_html_h1(self):
        markdown = "# This is a sentence with h1 heading"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [HTMLNode("h1", None, [LeafNode(None, "This is a sentence with h1 heading")])]))

    def test_markdown_to_html_h2(self):
        markdown = "## This is a sentence with h2 heading"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [HTMLNode("h2", None, [LeafNode(None, "This is a sentence with h2 heading")])]))

    def test_markdown_to_html_h3(self):
        markdown = "### This is a sentence with h3 heading"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [HTMLNode("h3", None, [LeafNode(None, "This is a sentence with h3 heading")])]))

    def test_markdown_to_html_h4(self):
        markdown = "#### This is a sentence with h4 heading"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [HTMLNode("h4", None, [LeafNode(None, "This is a sentence with h4 heading")])]))

    def test_markdown_to_html_h5(self):
        markdown = "##### This is a sentence with h5 heading"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [HTMLNode("h5", None, [LeafNode(None, "This is a sentence with h5 heading")])]))

    def test_markdown_to_html_h6(self):
        markdown = "###### This is a sentence with h6 heading"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None, [HTMLNode("h6", None, [LeafNode(None, "This is a sentence with h6 heading")])]))

    def test_markdown_to_html_ul(self):
        markdown = "* this is a list with\n* Multiple items\n- and both syntaxes"
        self.assertEqual(markdown_to_html_node(markdown), 
                         HTMLNode("div", None, 
                                    [HTMLNode("ul", None, 
                                        [HTMLNode("li", None, 
                                                [LeafNode(None, "this is a list with")]), 
                                        HTMLNode("li", None, 
                                                [LeafNode(None, "Multiple items")]), 
                                        HTMLNode("li", None, [LeafNode(None, "and both syntaxes")])])]))
        
    def test_markdown_to_html_ol(self):
        markdown = "1. this is a list with\n2. Multiple items\n3. and both syntaxes"
        self.assertEqual(markdown_to_html_node(markdown), 
                         HTMLNode("div", None, 
                                    [HTMLNode("ol", None, 
                                        [HTMLNode("li", None, 
                                                [LeafNode(None, "this is a list with")]), 
                                        HTMLNode("li", None, 
                                                [LeafNode(None, "Multiple items")]), 
                                        HTMLNode("li", None, [LeafNode(None, "and both syntaxes")])])]))
        

    def test_markdown_to_html_quote(self):
        markdown = ">This is a multiline quote \n>With multiple lines\n>and stuff"
        self.assertEqual(markdown_to_html_node(markdown), HTMLNode("div", None,
                                                                   [HTMLNode("blockquote", None,
                                                                             [[LeafNode(None, "This is a multiline quote ")],
                                                                                [LeafNode(None, "With multiple lines")],
                                                                                  [LeafNode(None, "and stuff")]])]))
        
    def test_markdown_to_html_paragraph(self):
        markdown = "This is a paragraph with *italic* and **bold**"
        self.assertEqual(markdown_to_html_node(markdown),
                         HTMLNode("div", None, 
                                  [HTMLNode("p", None,
                                            [LeafNode(None, "This is a paragraph with "),
                                             LeafNode("i", "italic"),
                                             LeafNode(None, " and "),
                                             LeafNode("b", "bold")])]))
        
       


if __name__ == "__main__":
    unittest.main()