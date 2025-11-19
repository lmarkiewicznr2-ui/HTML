class HTMLNode:
    def __init__(self, tag=None, value=None, props=None, children=None):
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children
    def to_html(self):
        raise NotImplementedError("")
    def props_to_html(self):
        props = []
        if not self.props:
            return ""
        for key, value in self.props.items():
            props.append(f'{key}="{value}"')
        return " " + " ".join(props)
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag is None:
            return str(self.value)
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        # Default children to empty list if not provided
        super().__init__(tag=tag, value=None, props=props, children=children if children is not None else [])

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent nodes must have a tag")
        if not self.children:
            raise ValueError("Parent nodes must have children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"