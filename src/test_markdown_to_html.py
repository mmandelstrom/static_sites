from block_funcs import *
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from inline_funcs import text_to_textnodes
from markdown_to_html import *
import unittest

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )
        
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html, "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
    def test_unordered_lists(self):
        md = """-First list item
-Second list item
-Third with **bold** and _italic_"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ul><li>First list item</li><li>Second list item</li><li>Third with <b>bold</b> and <i>italic</i></li></ul></div>"
        )

    def test_ordered_list(self):
        md = """1.First list item
2.Second list **bold**
3._Third_
4.And fourth"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>First list item</li><li>Second list <b>bold</b></li><li><i>Third</i></li><li>And fourth</li></ol></div>"
        )


    def test_h1(self):
        md = """# this is md with h1 and _italic_ and **bold** text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h1>this is md with h1 and <i>italic</i> and <b>bold</b> text</h1></div>"
        )

    def test_h2(self):
        md = """## this is md with h2 and _italic_ and **bold** text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h2>this is md with h2 and <i>italic</i> and <b>bold</b> text</h2></div>"
        )

    def test_h3(self):
        md = """### this is md with h3 and _italic_ and **bold** text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h3>this is md with h3 and <i>italic</i> and <b>bold</b> text</h3></div>"
        )

    def test_h4(self):
        md = """#### this is md with h4 and _italic_ and **bold** text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h4>this is md with h4 and <i>italic</i> and <b>bold</b> text</h4></div>"
        )

    def test_h5(self):
        md = """##### this is md with h5 and _italic_ and **bold** text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h5>this is md with h5 and <i>italic</i> and <b>bold</b> text</h5></div>"
        )

    def test_h6(self):
        md = """###### this is md with h6 and _italic_ and **bold** text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h6>this is md with h6 and <i>italic</i> and <b>bold</b> text</h6></div>"
        )

    def test_mixed_blocks(self):
        self.maxDiff = None
        md = """# Heading
    
Paragraph with **bold**
    
> A quote
    
- List item 1
- List item 2
    
```
code block```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><h1>Heading</h1><p>Paragraph with <b>bold</b></p><blockquote>A quote</blockquote><ul><li>List item 1</li><li>List item 2</li></ul><pre><code>code block</code></pre></div>"
            )
        
    def test_extract_title(self):
        md = """# This is my title, #### and some other stuff"""
        self.assertEqual(extract_title(md), "This is my title, #### and some other stuff")

    def test_extract_title_exception(self):
        md = "This is some markdown without a H1 header"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No H1 Header found")


if __name__ == "__main__":
    unittest.main()


