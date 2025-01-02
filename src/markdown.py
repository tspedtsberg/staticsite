from textnode import TextNode, TextType
import re
from blocktypes import (
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)
from htmlnode import ParentNode
from htmlnode import text_node_to_html_node


#list + delimeter + text type
def split_nodes_delimeter(old_nodes, delimeter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimeter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        """
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        result.extend(split_nodes)
    """
        
        for idx, strings in enumerate(sections):
            if strings == "":
                continue
            if idx % 2 == 0:
                split_nodes.append(TextNode(strings, TextType.TEXT))
            else:
                split_nodes.append(TextNode(strings, text_type))
        result.extend(split_nodes)
    return result
            
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    list_of_tuples = re.findall(pattern, text)
    return list_of_tuples

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    list_of_tuples = re.findall(pattern, text)
    return list_of_tuples
    # returnerer [("link", "https://boot.dev"), ("another link", "https://blog.boot.dev")]

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            result.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        original_text = node.text
        #extracts links from the original text with our previous function. this returns a list of tuples
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            #if theres no links, just append the node to the result
            result.append(node)
            continue
        for link in links:
            #splits the text into a lists sections by the link
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))
    return result    
    
def text_to_textnodes(text):
    tmp_node = [TextNode(text, TextType.TEXT)]
    tmp_node = split_nodes_delimeter(tmp_node, "**", TextType.BOLD)
    tmp_node = split_nodes_delimeter(tmp_node, "*", TextType.ITALIC)
    tmp_node = split_nodes_delimeter(tmp_node, "`", TextType.CODE)
    tmp_node = split_nodes_image(tmp_node)
    tmp_node = split_nodes_link(tmp_node)
    return tmp_node


#tager en raw string (represent a full document)
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for line in blocks:
        if line == "":
            continue
        line = line.strip()
        result.append(line)
    return result


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
    

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswitd("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_html_node(block):
    blocktype = block_to_block_type(block)
    if blocktype == block_type_paragraph:
        return paragraph_to_html_node(block)
    if blocktype == block_type_heading:
        return heading_to_html_node(block)
    if blocktype == block_type_code:
        return code_to_html_node(block)
    if blocktype == block_type_olist:
        return olist_to_html_node(block)
    if blocktype == block_type_ulist:
        return ulist_to_html_node(block)
    if blocktype == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")