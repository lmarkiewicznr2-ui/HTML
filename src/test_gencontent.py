from gencontent import gencontent
from textnode import TextNode, TextType
def test_gencontent_basic():
    text_nodes = [
        TextNode("Hello, world!", TextType.TEXT),
        TextNode("This is bold text.", TextType.BOLD),
        TextNode("This is italic text.", TextType.ITALIC),
        TextNode("print('Hello, World!')", TextType.CODE),
        TextNode("Click here", TextType.LINK, "https://www.example.com"),
        TextNode("An image", TextType.IMAGE, "https://www.example.com/image.png"),
    ]
    html_node = gencontent(text_nodes)
    assert html_node.tag == "div"
    assert len(html_node.children) == 6
    assert html_node.children[0].tag is None
    assert html_node.children[0].value == "Hello, world!"
    assert html_node.children[1].tag == "b"
    assert html_node.children[1].value == "This is bold text."
    assert html_node.children[2].tag == "i"
    assert html_node.children[2].value == "This is italic text."
    assert html_node.children[3].tag == "code"
    assert html_node.children[3].value == "print('Hello, World!')"
    assert html_node.children[4].tag == "a"
    assert html_node.children[4].value == "Click here"
    assert html_node.children[4].props == {"href": "https://www.example.com"}
    assert html_node.children[5].tag == "img"
    assert html_node.children[5].value == ""
    assert html_node.children[5].props == {
        "src": "https://www.example.com/image.png",
        "alt": "An image",
    }
def test_gencontent_empty():
    text_nodes = []
    html_node = gencontent(text_nodes)
    assert html_node.tag == "div"
    assert html_node.children == []
def test_gencontent_single_text_node():
    text_nodes = [TextNode("Single text node", TextType.TEXT)]
    html_node = gencontent(text_nodes)
    assert html_node.tag == "div"
    assert len(html_node.children) == 1
    assert html_node.children[0].tag is None
    assert html_node.children[0].value == "Single text node"
def test_gencontent_invalid_text_type():
    text_nodes = [TextNode("Invalid text type", "invalid_type")]
    try:
        gencontent(text_nodes)
        assert False, "Expected ValueError for invalid text type"
    except ValueError as e:
        assert str(e) == "invalid text type: invalid_type"