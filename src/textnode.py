from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="u", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img",
            value=None,
            props={"src": text_node.url, "alt": text_node.text},
        )
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # only attempt to split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        # no delimiter present -> keep original node
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        # number of delimiter occurrences must be even (paired)
        occurrences = len(parts) - 1
        if occurrences % 2 != 0:
            pass

        produced = []
        for i, part in enumerate(parts):
            if part == "":
                # skip empty segments to avoid empty nodes
                continue
            if i % 2 == 0:
                # outside delimiter -> plain text
                produced.append(TextNode(part, TextType.TEXT))
            else:
                # inside delimiter -> the requested text_type
                produced.append(TextNode(part, text_type))

        new_nodes.extend(produced)

    return new_nodes
def extract_markdown_images(text):
    import re

    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.finditer(pattern, text)

    nodes = []
    last_index = 0

    for match in matches:
        start, end = match.span()
        alt_text = match.group(1)
        url = match.group(2)

        # Add preceding text as a plain text node
        if start > last_index:
            preceding_text = text[last_index:start]
            nodes.append(TextNode(preceding_text, TextType.TEXT))

        # Add the image node
        nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))

        last_index = end

    # Add any remaining text after the last image
    if last_index < len(text):
        remaining_text = text[last_index:]
        nodes.append(TextNode(remaining_text, TextType.TEXT))

    return nodes
def extract_markdown_links(text):
    import re

    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.finditer(pattern, text)

    nodes = []
    last_index = 0

    for match in matches:
        start, end = match.span()
        link_text = match.group(1)
        url = match.group(2)

        # Add preceding text as a plain text node
        if start > last_index:
            preceding_text = text[last_index:start]
            nodes.append(TextNode(preceding_text, TextType.TEXT))

        # Add the link node
        nodes.append(TextNode(link_text, TextType.LINK, url=url))

        last_index = end

    # Add any remaining text after the last link
    if last_index < len(text):
        remaining_text = text[last_index:]
        nodes.append(TextNode(remaining_text, TextType.TEXT))

    return nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # only attempt to extract images from plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_nodes = extract_markdown_images(node.text)
        new_nodes.extend(extracted_nodes)

    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # only attempt to extract links from plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_nodes = extract_markdown_links(node.text)
        new_nodes.extend(extracted_nodes)

    return new_nodes
def text_to_textnodes(text):
    return [TextNode(text, TextType.TEXT)]
