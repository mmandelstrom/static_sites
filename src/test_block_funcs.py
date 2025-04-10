import unittest
from block_funcs import *

class TestBlock(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_more(self):
        md = """
            Heading

            This is a paragraph.

                - List item 1
                - List item 2

            Final block
            """
        self.assertEqual(markdown_to_blocks(md), [
            'Heading', 
            'This is a paragraph.',
              '- List item 1\n- List item 2',
              'Final block'
              ])
        
    def test_markdown_to_blocks_empty(self):
        md = """
            

            """
        self.assertEqual(markdown_to_blocks(md), [])


    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
            Heading



            A paragraph

                -List item 1
                -List item 2
                -List item 3



            another paragraph
            """
        self.assertEqual(markdown_to_blocks(md), [
            'Heading',
            'A paragraph',
            '-List item 1\n-List item 2\n-List item 3',
            'another paragraph'
        ])

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single line"
        self.assertEqual(markdown_to_blocks(md), ["This is a single line"])

    def test_markdown_to_blocks_excessive_whitespace(self):
        md = """
                    Heading with some whitespace    
                
                and a paragraph with some

                            -And a a list
                            -with two lines
            """
        self.assertEqual(markdown_to_blocks(md), [
            "Heading with some whitespace",
            "and a paragraph with some",
            "-And a a list\n-with two lines"
        ])

    def test_markdown_to_blocks_different_list_icons(self):
        md = """
            


            Heading

            *List item 1
            &List item 2
            ?List item 3




            """
        self.assertEqual(markdown_to_blocks(md), [
            "Heading",
            "*List item 1\n&List item 2\n?List item 3"
        ])

    def test_markdown_to_blocks_only_blank_lines(self):
        md = "\n\n\n\n"
        self.assertEqual(markdown_to_blocks(md), [])


    def test_markdown_to_blocks_nested_content(self):
        md = """
        Parent List:
        - Item A:
            - Subitem A1
            - Subitem A2
            
        Another paragraph
        """
        self.assertEqual(markdown_to_blocks(md), [
            "Parent List:\n- Item A:\n- Subitem A1\n- Subitem A2",
            "Another paragraph"
        ])

    def test_markdown_to_blocks_whitespace_blocks(self):
        md = """
        Heading
        
        \n       
        Another block
        """
        self.assertEqual(markdown_to_blocks(md), [
            "Heading",
            "Another block"
        ])

    def test_block_to_block_type_heading_1(self):
        block = """# This is a heading wit some text etx"""
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_2(self):
        block = """## This is a h2"""
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_heading_3(self):
        block = """### This is a h3"""
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_4(self):
        block = """#### This is a h4"""
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_5(self):
        block = """##### This is a h5"""
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_6(self):
        block = """###### This is a h6"""
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_inavlid_heading(self):
        block = """####### this should become paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = """```This is a codeblock ```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_invalid_code_end(self):
        block = """```This is invalid``"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_code_start(self):
        block = "``This is also invalid```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = """> First quote
>second
> third
>   fourth"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_invalid_quote(self):
        block = """
>this is invalid as first line does not have >"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = """-this
-is
-a
-list"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_invalid(self):
        block = """-list
*but not
-correct"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_invalid_2(self):
        block = """*not
-a
-valid
list"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = """1. This
2. Is
3. A
4. List
5. !!!"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_invalid(self):
        block = """1. This
3. Is
2. Invalid"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_invalid_2(self):
        block = """1. Also
*Invalid
2. List"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        block = """This is a paragraph"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()