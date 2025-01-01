from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        #to be overwritten by child
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        
        lst = []
        for key, value in self.props.items():
            lst.append(f' {key}="{value}"')
        #retunerer indholdet af listen med "".join(). 
        return "".join(lst)
    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return (f"{self.value}")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag:{self.tag}, value:{self.value}, props:{self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        if self.children is None:
            raise ValueError("invalid children, missing input")
        tmp_list = ""
        for child in self.children:
           tmp_list += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{tmp_list}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(None, text_node.text)
        return node
    elif text_node.text_type == TextType.BOLD:
        node = LeafNode("b", text_node.text)
        return node
    elif text_node.text_type == TextType.ITALIC:
        node = LeafNode("i", text_node.text)
        return node
    elif text_node.text_type == TextType.CODE:
        node = LeafNode("code", text_node.text)
        return node
    elif text_node.text_type == TextType.LINK:
        node = LeafNode("a", text_node.text, {"href": text_node.url})
        return node
    elif text_node.text_type == TextType.IMAGE:
        node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        return node
    else: 
        raise Exception("Invalid text_type. text_type has to be in TextType Enum")
    

