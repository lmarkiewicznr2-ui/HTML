import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_neq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_neq_different_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
    def test_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "u")
        self.assertEqual(html_node.value, "This is code text")
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "An image"},
        )
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("Hello, world! This is a test.", TextType.TEXT),
            TextNode("This should not be split.", TextType.BOLD),
        ]
        delimiter = " "
        text_type = TextType.TEXT

        expected_new_nodes = [
            TextNode("Hello,", TextType.TEXT),
            TextNode("world!", TextType.TEXT),
            TextNode("This", TextType.TEXT),
            TextNode("is", TextType.TEXT),
            TextNode("a", TextType.TEXT),
            TextNode("test.", TextType.TEXT),
            TextNode("This should not be split.", TextType.BOLD),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(new_nodes, expected_new_nodes)
    def test_extract_markdown_images(self):
        markdown_text = "Here is an image: ![Alt text](https://example.com/image.png)"
        expected_nodes = [
            TextNode("Here is an image: ", TextType.TEXT),
            TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png"),
        ]

        nodes = extract_markdown_images(markdown_text)
        self.assertEqual(nodes, expected_nodes)
    def test_extract_markdown_links(self):
        markdown_text = "Here is a link: [Example](https://example.com)"
        expected_nodes = [
            TextNode("Here is a link: ", TextType.TEXT),
            TextNode("Example", TextType.LINK, "https://example.com"),
        ]

        nodes = extract_markdown_links(markdown_text)
        self.assertEqual(nodes, expected_nodes)
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
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )
    def test_split_no_images_or_links(self):
        node = TextNode("This is plain text without images or links.", TextType.TEXT)
        new_nodes_image = split_nodes_image([node])
        new_nodes_link = split_nodes_link([node])
        self.assertListEqual([node], new_nodes_image)
        self.assertListEqual([node], new_nodes_link)
    def test_text_to_textnodes(self):
        text = "This is **bold** and *italic* text with `code`."
        expected_nodes = [
            TextNode("This is **bold** and *italic* text with `code`.", TextType.TEXT),
        ]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)
    def test_text_to_textnodes_with_images_and_links(self):
        text = "Here is an image ![Alt](https://example.com/image.png) and a link [Example](https://example.com)."
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("Alt", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and a link ", TextType.TEXT),
            TextNode("Example", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        nodes = text_to_textnodes(text)
        # ensure images and links are split out into separate nodes
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        self.assertEqual(nodes, expected_nodes)
    def test_text_to_textnodes_empty(self):
        text = ""
        expected_nodes = [TextNode("", TextType.TEXT)]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()