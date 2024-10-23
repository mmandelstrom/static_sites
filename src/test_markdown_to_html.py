import unittest

from textnode import *
from htmlnode import *
from markdown_to_html import *

class TestHTMLNode(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode('This is the value **with bold** inside of it', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode('This is the value ', TextType.TEXT), TextNode('with bold', TextType.BOLD), TextNode(' inside of it', TextType.TEXT)])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode('This is the value *with italic* inside of it', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), [TextNode('This is the value ', TextType.TEXT), TextNode('with italic', TextType.ITALIC), TextNode(' inside of it', TextType.TEXT)])

    def test_split_nodes_delimiter_code(self):
        node = TextNode('This is the value `code` inside of it', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [TextNode('This is the value ', TextType.TEXT), TextNode('code', TextType.CODE), TextNode(' inside of it', TextType.TEXT)])

    def test_split_nodes_delimiter_multiple_nodes(self):
        nodes = [
            TextNode('This first node **with a bold sentence**', TextType.TEXT),
            TextNode('This is the second node *with italic sentence* inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
        ]
        with_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        with_italic = split_nodes_delimiter(with_bold, "*", TextType.ITALIC)
        with_code = split_nodes_delimiter(with_italic, "`", TextType.CODE)
        self.assertEqual(with_bold, [
            TextNode('This first node ', TextType.TEXT),
            TextNode('with a bold sentence', TextType.BOLD),
            TextNode('This is the second node *with italic sentence* inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
            ])

    def test_split_nodes_no_end_delimiter(self):
        node = [TextNode('this is the text **without ending delimiter*', TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(node, "**", TextType.BOLD)

    def test_split_nodes_no_delimiter(self):
        node = [TextNode('this is the text without delimiter', TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), [TextNode('this is the text without delimiter', TextType.TEXT)])

    def test_split_nodes_nested_no_delimiter(self):
        nodes = [
            TextNode('This first node **with a bold sentence**', TextType.TEXT),
            TextNode('This is the second node with a normal sentence inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
        ]
        with_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        with_italic = split_nodes_delimiter(with_bold, "*", TextType.ITALIC)
        with_code = split_nodes_delimiter(with_italic, "`", TextType.CODE)
        self.assertEqual(with_bold, [
            TextNode('This first node ', TextType.TEXT),
            TextNode('with a bold sentence', TextType.BOLD),
            TextNode('This is the second node with a normal sentence inside of it', TextType.TEXT),
            TextNode('This is the third node `with code` inside of it', TextType.TEXT)
            ])

    def test_split_nodes_start_with_delimiter(self):
        node = TextNode('**with bold** text after', TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode('with bold', TextType.BOLD), TextNode(' text after', TextType.TEXT)])


#Test for extract_markdown_images & extract_markdown_link functions

    def test_extract_markdown_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_link_incorrcet_syntax(self):
        text = "This is text with a link [to [boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to [boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])  




#Test split_markdown_image and split_markdown_link

    def test_split_nodes_link_multiple_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'), 
            TextNode(' and ', TextType.TEXT),
            TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev')])
        
    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [this is the alt text](https://imgur.com/link)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('this is the alt text', TextType.LINK, 'https://imgur.com/link')
        ])
        
    def test_split_nodes_link_multiple_nodes(self):

        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        node2 = TextNode("This is the second node in list with link to [google](https://google.se)", TextType.TEXT)
        node3 = TextNode("This is the third node with link to [imgur](https://imgur.com)", TextType.TEXT)

        self.assertEqual(split_nodes_link([node,node2,node3]), [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('to boot dev', TextType.LINK, 'https://www.boot.dev'),
            TextNode(' and ', TextType.TEXT),
            TextNode('to youtube', TextType.LINK, 'https://www.youtube.com/@bootdotdev'),
            TextNode('This is the second node in list with link to ', TextType.TEXT),
            TextNode('google', TextType.LINK, 'https://google.se'),
            TextNode('This is the third node with link to ', TextType.TEXT),
            TextNode('imgur', TextType.LINK, 'https://imgur.com')
        ])

    def test_split_nodes_link_three_links(self):
        node = TextNode('[first alt](https://first_link.com) and then some text [second alt](https://second_link.com) and some more text [](https://third_link.com)', TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode('first alt', TextType.LINK, 'https://first_link.com'),
            TextNode(' and then some text ', TextType.TEXT),
            TextNode('second alt', TextType.LINK, 'https://second_link.com'),
            TextNode(' and some more text ', TextType.TEXT),
            TextNode('', TextType.LINK, 'https://third_link.com')
        ])


    def test_split_nodes_link_missing_alt_text(self):
        node = TextNode("This is text with a link [](https://www.youtube.com)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode('This is text with a link ', TextType.TEXT),
            TextNode('', TextType.LINK, 'https://www.youtube.com')])
    


    def test_split_nodes_link_empty_link_and_alt_text(self):
        node = TextNode("This is text with a link []()", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_link([node])
        self.assertEqual(str(context.exception), "Invalid input: Missing URL.")


    def test_split_nodes_link_empty_link(self):
        node = TextNode("This is text with a link [alt text]()", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_link([node])
        self.assertEqual(str(context.exception), "Invalid input: Missing URL.")

    def test_split_nodes_link_no_link(self):
        node = TextNode("This is text with a link with some characters etc(", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])



    def test_split_nodes_image(self):
        node = TextNode("This is text with an image ![this is the alt text](https://imgur.com/image)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("this is the alt text", TextType.IMAGE, "https://imgur.com/image")
        ])

    def test_split_nodes_image_multiple_iamges(self):
        node = TextNode("This is text with an image ![this is the alt text](https://imgur.com/image) and this is the second image ![second alt text](https://www.url_to_image.com/image) and some space after", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode('This is text with an image ', TextType.TEXT),
            TextNode('this is the alt text', TextType.IMAGE, 'https://imgur.com/image'),
            TextNode(' and this is the second image ', TextType.TEXT),
            TextNode('second alt text', TextType.IMAGE, 'https://www.url_to_image.com/image'),
            TextNode(' and some space after', TextType.TEXT)
        ])
        

    def test_split_nodes_image_multiple_nodes(self):
        node = TextNode("This is text with an image ![this is the alt text](https://imgur.com/image)", TextType.TEXT)
        node2 = TextNode("This is the second node ![my image](https://www.url_to_my_image.com/image)", TextType.TEXT)
        node3 = TextNode("This is the third node ![alt_text](https://some_random_url.ru/virus)", TextType.TEXT)

        self.assertEqual(split_nodes_image([node, node2, node3]), [
            TextNode('This is text with an image ', TextType.TEXT),
            TextNode('this is the alt text', TextType.IMAGE, 'https://imgur.com/image'),
            TextNode('This is the second node ', TextType.TEXT),
            TextNode('my image', TextType.IMAGE, 'https://www.url_to_my_image.com/image'),
            TextNode('This is the third node ', TextType.TEXT),
            TextNode('alt_text', TextType.IMAGE, 'https://some_random_url.ru/virus')
        ])


    def test_split_nodes_image_missing_alt_text(self):
        node = TextNode('This is text ![](https://imgur.com/image)', TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode('This is text ', TextType.TEXT),
            TextNode('', TextType.IMAGE, 'https://imgur.com/image')
        ])

    def test_split_nodes_image_missing_url(self):
        node = TextNode('This is text ![alt text]()', TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_image([node])
        self.assertEqual(str(context.exception), "Invalid input: Missing URL.")

    def test_split_nodes_image_invalid_syntax(self):
        node = TextNode('This is the invalid syntax ![)', TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_split_nodes_image_three_images(self):
        node = TextNode('![](https://url_to_first.image) some filler ![alt text](https://url_to_second.image)![more alt text](https://url_to_third_image)', TextType.TEXT)
        self.assertEqual(split_nodes_image([node]),[
            TextNode("", TextType.IMAGE, 'https://url_to_first.image'),
            TextNode(' some filler ', TextType.TEXT),
            TextNode('alt text', TextType.IMAGE, 'https://url_to_second.image'),
            TextNode('more alt text', TextType.IMAGE, 'https://url_to_third_image')
        ])

if __name__ == "__main__":
    unittest.main()