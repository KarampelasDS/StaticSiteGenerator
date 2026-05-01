import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.BOLD, None)")
        
    def test_link_node(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.example.com")
        self.assertEqual(node.text, "This is a link")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://www.example.com")
        
        
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "This is plain text")
        
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")
        
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This is a link", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.example.com">This is a link</a>')


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_bold_delimiter(self):
        old_nodes = [
            TextNode("**This is some bold text**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is some bold text", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_nodes_italic_delimiter(self):
        old_nodes = [
            TextNode("*This is some italic text*", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is some italic text", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_code_delimiter(self):
        old_nodes = [
            TextNode("`This is some code text`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is some code text", TextType.CODE)
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_normal_text(self):
        old_nodes = [
            TextNode("This is some normal text", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.TEXT)
        expected_nodes = [
            TextNode("This is some normal text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
    def test_split_nodes_no_delimeter_matches(self):
        old_nodes = [
            TextNode("*This is some italic text*", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("*This is some italic text*", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()