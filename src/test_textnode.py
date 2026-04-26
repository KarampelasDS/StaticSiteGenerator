import unittest

from textnode import TextNode, TextType


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
        


if __name__ == "__main__":
    unittest.main()