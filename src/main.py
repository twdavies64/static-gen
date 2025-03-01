import sys
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_nodes import text_to_textnodes
from block_markdown import markdown_to_blocks
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)


def main():
    print("You pass butter")

    # md = """
    # ```python
    # def hello_world():
    #     print("Hello, world!")
    # ```

    # Next block here.
    # """
    # blocks = markdown_to_blocks(md)
    # print(blocks)

    # text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    # print(text_to_textnodes(text))

    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # print(extract_markdown_images(text))

    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))

    # node = TextNode(
    #     "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #     TextType.TEXT,
    # )
    # new_nodes = split_nodes_link([node])
    # print(new_nodes)

    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    # node = TextNode("This is text with some **very bold** words", TextType.TEXT)
    # new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    # print(new_nodes)

    # print(text_node_to_html_node(text_node))

    # bob = TextNode("This is only a test", TextType.BOLD, "https://www.boot.dev")
    # link = HTMLNode(
    #     "a",
    #     "blah blah blah blah",
    #     "",
    #     {
    #         "href": "https://www.google.com",
    #         "target": "_blank",
    #     },
    # )
    # lief = LeafNode("p", "This is some text for this paragraph")
    # link_test = LeafNode(
    #     "a", "Clicky clicky!", {"href": "https://www.google.com", "target": "_blank"}
    # )

    # node = ParentNode(
    #     "p",
    #     [
    #         LeafNode("b", "Bold text"),
    #         LeafNode(None, "Normal text"),
    #         LeafNode("i", "italic text"),
    #         LeafNode(None, "Normal text"),
    #     ],
    # )

    # print(bob)
    # print(link)
    # print(link.props_to_html())
    # print(lief.to_html())
    # print(link_test.to_html())

    # print(node.to_html())

    return 0


if __name__ == "__main__":
    sys.exit(main())
