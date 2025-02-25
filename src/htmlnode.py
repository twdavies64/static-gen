SELF_CLOSING_TAGS = {
    "img",
    "br",
    "hr",
    "input",
    "meta",
    "link",
    "base",
    "area",
    "col",
    "embed",
    "source",
    "track",
    "wbr",
}


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(
            list(map(lambda item: f' {item[0]}="{item[1]}"', self.props.items()))
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None and self.tag not in SELF_CLOSING_TAGS:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.tag in SELF_CLOSING_TAGS:
            return f"<{self.tag}{self.props_to_html()} />"
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
