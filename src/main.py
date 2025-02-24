import sys
from textnode import TextNode, TextType
from htmlnode import HTMLNode


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
    print(bob)
    print(link)
    print(link.props_to_html())

    return 0


if __name__ == "__main__":
    sys.exit(main())
