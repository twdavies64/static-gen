import sys
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def main():
    bob = TextNode("This is only a test", TextType.BOLD, "https://www.boot.dev")
    link = HTMLNode(
        "a",
        "blah blah blah blah",
        "",
        {
            "href": "https://www.google.com",
            "target": "_blank",
        },
    )
    lief = LeafNode("p", "This is some text for this paragraph")
    link_test = LeafNode(
        "a", "Clicky clicky!", {"href": "https://www.google.com", "target": "_blank"}
    )
    print(bob)
    print(link)
    print(link.props_to_html())
    print(lief.to_html())
    print(link_test.to_html())

    return 0


if __name__ == "__main__":
    sys.exit(main())
