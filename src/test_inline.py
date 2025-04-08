import unittest
from inline_funcs import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_link, split_nodes_image
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

class TestInline(unittest.TestCase):

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is some text with a **bold** word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is some text with a _italic_ word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is some text with a `code` word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ])

    def test_split_nodes_delimiter_multiple_bold(self):
        node = TextNode("This is some text with a **bold** word and **another** word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
            ])

    def test_split_nodes_delimiter_multiple_italic(self):
        node = TextNode("This is some text with a _italic_ word and _italic_ word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
            ])

    def test_split_nodes_delimiter_multiple_code(self):
        node = TextNode("This is some text with a `code` word and `code` word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_no_closing_bold(self):
        node = TextNode("This is some text with a **bold* word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), f"No closing delimiter found for **")

    def test_split_nodes_delimiter_no_closing_italic(self):
        node = TextNode("This is some text with a _italic word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(str(context.exception), f"No closing delimiter found for _")

    def test_split_nodes_delimiter_no_closing_code(self):
        node = TextNode("This is some text with a `code word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), f"No closing delimiter found for `")

    def test_split_nodes_delimiter_invalid_delimiter(self):
        node = TextNode("This is some text with *invalid* delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(str(context.exception), f"* is not a valid markdown delimiter")

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode("This is some text with a `code word`", TextType.TEXT),
            TextNode("This is the second with `code`", TextType.TEXT),
            TextNode("`code` words etc", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), [
            TextNode("This is some text with a ", TextType.TEXT),
            TextNode("code word", TextType.CODE),
            TextNode("This is the second with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("code", TextType.CODE),
            TextNode(" words etc", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_start_and_end(self):
        node = TextNode("**bold** word in the start and **end**", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("bold", TextType.BOLD),
            TextNode(" word in the start and ", TextType.TEXT),
            TextNode("end", TextType.BOLD)
        ])

    def test_split_nodes_delimiter_start_italic(self):
        node = TextNode("_italic words_ in the beginning", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
            TextNode("italic words", TextType.ITALIC),
            TextNode(" in the beginning", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_end_code(self):
        node = TextNode("sentence ending with `code`", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
            TextNode("sentence ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ])

    def test_split_nodes_delimiter_no_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [
            TextNode("", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_text_type_image(self):
        node = TextNode("image of fun stuff", TextType.IMAGE, "https://image.com")
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.IMAGE), [
            TextNode("image of fun stuff", TextType.IMAGE, "https://image.com")
        ])

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
        "This is text with an [to boot dev](https://www.boot.dev))"
    )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is some text with ![image](image.com) and some more text with ![img](img.img) and so on"
        )
        self.assertListEqual([("image", "image.com"), ("img", "img.img")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is a link [google](google.com) and some text [boot dev](boot.dev) and text"
        )
        self.assertListEqual([("google", "google.com"), ("boot dev", "boot.dev")], matches)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ])

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](www.image.com) and another ![picture](https://www.picture.com)",
            TextType.TEXT
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "www.image.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("picture", TextType.IMAGE, "https://www.picture.com")
        ])

    def test_split_nodes_link_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        ])

    def test_split_nodes_image(self):
        node = TextNode(
            "![image](https://www.image.com)",
            TextType.TEXT
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("image", TextType.IMAGE, "https://www.image.com")
        ])
    
    def test_split_nodes_link_end(self):
        node = TextNode(
            "This is node ending with [link](https://www.boot.dev)", TextType.TEXT
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is node ending with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ])

    def test_split_nodes_image_end(self):
        node = TextNode(
            "This is a node ending with ![image](https://www.image.com)", TextType.TEXT
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is a node ending with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.image.com")
        ])

    def test_split_nodes_no_image(self):
        node = TextNode(
            "This is a node without image", TextType.TEXT
        )
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is a node without image", TextType.TEXT)
        ])

    def test_split_nodes_no_link(self):
        node = TextNode(
            "This is a node without link", TextType.TEXT
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is a node without link", TextType.TEXT)
        ])

    def test_split_nodes_link_type_link(self):
        node = TextNode(
            "![link](https://www.link.com)", TextType.LINK
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("![link](https://www.link.com)", TextType.LINK)
        ])

    def test_split_nodes_image_type_image(self):
        node = TextNode(
            "[image](https://www.image.com)", TextType.IMAGE
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("[image](https://www.image.com)", TextType.IMAGE)
        ])

    def test_split_nodes_image_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [])

    def test_split_nodes_link_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [])

    def test_split_nodes_image_multiple_nodes(self):
        node = TextNode("this is the first node with ![image](https://first.image)", TextType.TEXT)
        node2 = TextNode("this is the second node with ![image](https://second.image) and more text", TextType.TEXT)
        node3 = TextNode("this is the third node with ![image](https://third.image)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node, node2, node3]), [
            TextNode("this is the first node with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://first.image"),
            TextNode("this is the second node with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://second.image"),
            TextNode(" and more text", TextType.TEXT),
            TextNode("this is the third node with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://third.image")
        ])

    def test_split_nodes_link_multiple_nodes(self):
        node = TextNode("This is the first node with a [link](https://www.google.se)", TextType.TEXT)
        node2 = TextNode("Second node with link to [boot dev](https://www.boot.dev) and [youtube](https://www.youtube.com) and some text", TextType.TEXT)
        node3 = TextNode("This node should be added as is", TextType.BOLD)
        node4 = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_link([node, node2, node3, node4]), [
            TextNode("This is the first node with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.se"),
            TextNode("Second node with link to ", TextType.TEXT),
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
            TextNode(" and some text", TextType.TEXT),
            TextNode("This node should be added as is", TextType.BOLD)
        ])

if __name__ == "__main__":
    unittest.main()
