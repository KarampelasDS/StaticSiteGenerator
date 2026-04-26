import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
        
    def test_repr(self):
        node = HTMLNode("div",  "testContent", [])
        self.assertEqual(repr(node), "HTMLNode(div, testContent, [], None)")
        
    def test_props_to_html(self):
        node = HTMLNode("div",  "testContent", [], {"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')
    
    def test_props_to_html_none(self):
        node = HTMLNode("div",  "testContent", [], None)
        self.assertEqual(node.props_to_html(), '')