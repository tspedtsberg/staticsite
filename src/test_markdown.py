import unittest

from markdown import (
    split_nodes_delimeter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title,
)

from blocktypes import (
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)
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
        self.assertListEqual(output,[
            ("link", "https://boot.dev"),
            ("another link", "https://blog.boot.dev")
        ])

    def test_split_nodes_images(self):
        text_node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
        TextType.TEXT,)
        new_node = split_nodes_image([text_node])
        self.assertListEqual([TextNode("This is text with a ", TextType.TEXT),
                              TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                              TextNode(" and ", TextType.TEXT),
                              TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
                              ], new_node)

    def test_split_nodes_image(self):
        text_node = TextNode("this is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and it looks cool af", TextType.TEXT, )
        new_node = split_nodes_image([text_node])
        self.assertListEqual([TextNode("this is a text with a ", TextType.TEXT),
                              TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                              TextNode(" and it looks cool af", TextType.TEXT)],
                              new_node)
        
    def test_split_nodes_image_single(self):
        node = TextNode("![cool image af](https://www.example.com/IMAGE.PNG)", TextType.TEXT, )
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode("cool image af", TextType.IMAGE, "https://www.example.com/IMAGE.PNG")],
                             new_node)
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ], output)
        

    def test_markdown_to_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        output = markdown_to_blocks(text)
        self.assertEqual([
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ], output)


    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)


    def test_extract_title(self):
        markdown = '''# My Title
        Some other text.
        ## A sub-title

        More content here...
        '''
        header = extract_title(markdown)
        self.assertEqual(header, "# My Title")

if __name__ == "__main__":
    unittest.main()