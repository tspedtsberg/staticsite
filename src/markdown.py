from textnode import TextNode, TextType
import re

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
