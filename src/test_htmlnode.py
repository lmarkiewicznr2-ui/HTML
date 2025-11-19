import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
class TestHtmlNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(tag="div", value="Hello", props={"class": "greeting"}, children=[])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {"class": "greeting"})
        self.assertEqual(node.children, [])
    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"class": "my-class", "id": "my-id"})
        expected_html = ' class="my-class" id="my-id"'
        self.assertEqual(node.props_to_html(), expected_html)
    def test_props_to_html_without_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    def test_repr(self):
        node = HTMLNode(tag="span", value="Text", props={"style": "color:red"}, children=[])
        expected_repr = "HTMLNode(tag=span, value=Text, props={'style': 'color:red'}, children=[])"
        self.assertEqual(repr(node), expected_repr)
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(value="Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    def test_leaf_to_html_no_value(self):
        node = LeafNode("span")
        with self.assertRaises(ValueError):
            node.to_html()
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(children=[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div")
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()