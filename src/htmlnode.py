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
        if props is not None and not isinstance(props, dict):
            raise TypeError("props must be a dict")
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
            list(
                map(
                    lambda item: f' {item[0]}="{item[1].replace('"', "&quot;" )}"',
                    self.props.items(),
                )
            )
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None and tag not in SELF_CLOSING_TAGS:
            raise ValueError("value is required for non-self-cloding tags")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        if self.tag in SELF_CLOSING_TAGS:
            return f"<{self.tag}{self.props_to_html()} />"
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("tag is required for ParentNode")
        if not children:
            raise ValueError("children are required for ParentNode")
        if not isinstance(children, list):
            raise TypeError("children must be a list")
        filtered_children = list(filter(lambda x: x is not None, children))
        if not filtered_children:
            raise ValueError("all children are None")
        super().__init__(tag=tag, value=None, children=filtered_children, props=props)

    def to_html(self):
        par_str = ""
        for child in self.children:
            par_str += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{par_str}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
