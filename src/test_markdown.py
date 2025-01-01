import unittest

from markdown import split_nodes_delimeter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class testmarkdown(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("this is text with a `code block` word", TextType.TEXT)
        new_list = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertListEqual(new_list, (
            [TextNode("this is text with a ",TextType.TEXT),
             TextNode("code block", TextType.CODE),
             TextNode(" word", TextType.TEXT)]
        ))

    def test_delim_bold(self):
        node = TextNode("this is a text with a **bolded** word", TextType.TEXT)
        new_list = split_nodes_delimeter([node], "**", TextType.BOLD)
        self.assertListEqual(new_list, (
            [TextNode("this is a text with a ", TextType.TEXT),
             TextNode("bolded", TextType.BOLD),
             TextNode(" word", TextType.TEXT)]
        ))
    
    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimeter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )


    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimeter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


class Testextract_markdown_images(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = extract_markdown_images(text)
        self.assertListEqual(output, 
                             [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


    def test_extract_markdown_link(self):
        text = "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        output = extract_markdown_links(text)


if __name__ == "__main__":
    unittest.main()