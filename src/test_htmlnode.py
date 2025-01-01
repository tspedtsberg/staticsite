import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        # Set up a test case with some props
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://google.com\" target=\"_blank\"")
        
    def test_props_to_html(self):
        node = HTMLNode(props={"test": "greet", "href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), " test=\"greet\" href=\"https://boot.dev\"")


    def test_value(self):
        node = HTMLNode("div", "I wish I could read",)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")


    def test_repr(self):
        node = HTMLNode("p", "What a wierd world", None, {"class": "primary"})
        self.assertEqual(node.__repr__(), "HTMLNode(tag:p, value:What a wierd world, children:None, props:{'class': 'primary'})")


    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello world!")
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("span", "grandchild1")
        grandchild_node2 = LeafNode("span", "grandchild2")
        child_node = ParentNode("b", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><b><span>grandchild1</span><span>grandchild2</span></b></div>")
        
    def test_text_node_to_html_node(self):
        text_node = TextNode("tester", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "tester")




if __name__ == "__main__":
    unittest.main()
