import unittest
from textnode import TextNode
from textnode import TextType
from inline_markdown import split_nodes_delimiter
from inline_markdown import extract_markdown_images
from inline_markdown import extract_markdown_links
from inline_markdown import split_nodes_image
from inline_markdown import split_nodes_link
from inline_markdown import text_to_textnodes

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
            TextNode("_This is some italic text_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
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
            TextNode("_This is some italic text_", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("_This is some italic text_", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is an image: ![alt text](image_url)"
        matches = extract_markdown_images(text)
        expected_matches = [("alt text", "image_url")]
        self.assertEqual(matches, expected_matches)
        
    def test_extract_markdown_images_no_matches(self):
        text = "Here is some text without images."
        matches = extract_markdown_images(text)
        expected_matches = []
        self.assertEqual(matches, expected_matches)
        
    def test_extract_markdown_images_multiple_matches(self):
        text = "Here are some images: ![alt text 1](image_url_1) and ![alt text 2](image_url_2)"
        matches = extract_markdown_images(text)
        expected_matches = [("alt text 1", "image_url_1"), ("alt text 2", "image_url_2")]
        self.assertEqual(matches, expected_matches)
        
    def test_extract_markdown_images_no_arguments(self):
        text = "Here is an image with no arguments: ![]()"
        matches = extract_markdown_images(text)
        expected_matches = [("", "")]
        self.assertEqual(matches, expected_matches)

    def test_extract_markdown_images_ignore_links(self):
        text = "Here is an image and a link: ![alt text](image_url) and [link text](link_url)"
        matches = extract_markdown_images(text)
        expected_matches = [("alt text", "image_url")]
        self.assertEqual(matches, expected_matches)
        
    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](link_url)"
        matches = extract_markdown_links(text)
        expected_matches = [("link text", "link_url")]
        self.assertEqual(matches, expected_matches)
        
    def test_extract_markdown_links_no_matches(self):
        text = "Here is some text without links."
        matches = extract_markdown_links(text)
        expected_matches = []
        self.assertEqual(matches, expected_matches)
        
    def test_extract_markdown_links_multiple_matches(self):
        text = "Here are some links: [link text 1](link_url_1) and [link text 2](link_url_2)"
        matches = extract_markdown_links(text)
        expected_matches = [("link text 1", "link_url_1"), ("link text 2", "link_url_2")]
        self.assertEqual(matches, expected_matches)
    
    def test_extract_markdown_links_no_arguments(self):
        text = "Here is a link with no arguments: []()"
        matches = extract_markdown_links(text)
        expected_matches = [("", "")]
        self.assertEqual(matches, expected_matches)
        
    def test_extract_markdown_links_ignore_images(self):
        text = "Here is a link and an image: [link text](link_url) and ![alt text](image_url)"
        matches = extract_markdown_links(text)
        expected_matches = [("link text", "link_url")]
        self.assertEqual(matches, expected_matches)
        
class TestImageLinkSplit(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is some **bold** text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected_nodes)
    
    def test_text_to_textnodes_no_markdown(self):
        text = "This is some normal text without markdown."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is some normal text without markdown.", TextType.TEXT)
        ]
        self.assertListEqual(nodes, expected_nodes)
        
    def test_text_to_textnodes_multiple_markdown(self):
        text = "This is **bold** and _italic_ text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected_nodes)
    
    

if __name__ == "__main__":
    unittest.main()