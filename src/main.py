import sys
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_nodes import text_to_textnodes
from block_markdown import markdown_to_blocks
from blocknode import markdown_to_html_node
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
    # > - Item 1
    # > - Item 2 with **bold** text
    # """
    # node = markdown_to_html_node(md)
    # print(node.to_html())
    # print("<div><blockquote><ul><li>Item 1</li><li>Item 2 with <b>bold</b> text</li></ul></blockquote></div>")

    # # Case 1: Debug blockquote
    # md_1 = """
    # > This is a blockquote with multiple lines and some **bold** and _italic_ text and even some `code` too
    # """
    # node_1 = markdown_to_html_node(md_1)
    # print("Case 1 - Blockquote:\n", node_1.to_html())

    # # Case 2: Debug consecutive same blocks
    # md_2 = """
    # # First Heading

    # # Second Heading

    # > First quote

    # > Second quote
    # """
    # node_2 = markdown_to_html_node(md_2)
    # print("\nCase 2 - Consecutive Same Blocks:\n", node_2.to_html())

    # # md = """
    # # #

    # # >

    # # ```
    # # ```

    # # -
    # # """
    # # node = markdown_to_html_node(md)
    # # print("\nCase 3 - Empty Blocks:\n", node.to_html())

    # # Case 4: Debug mixed content
    # md_4 = """
    # # Document Title

    # > Important quote with formatting in **bold**

    # Regular paragraph.
    # ```
    # code block
    # with multiple lines
    # ```

    # - List item 1
    # - List item 2
    # """
    # node_4 = markdown_to_html_node(md_4)
    # print("\nCase 4 - Mixed Content:\n", node_4.to_html())

    # # Case 5: Debug nested blockquotes
    # md_5 = """
    # > This is a blockquote

    # > > Nested blockquote
    # """
    # node_5 = markdown_to_html_node(md_5)
    # print("\nCase 5 - Nested Blockquotes:\n", node_5.to_html())

    # # Case 6: Debug nested inline elements
    # md_6 = """
    # This is a paragraph with **bold text that contains `code` and _italic_ parts** inside it.
    # """
    # node_6 = markdown_to_html_node(md_6)
    # print("\nCase 6 - Nested Inline Elements:\n", node_6.to_html())

    # # Case 7: Debug whitespace handling
    # md_7 = """
    # # Heading with spaces

    # Paragraph with  multiple   spaces  and

    # newlines
    # """
    # node_7 = markdown_to_html_node(md_7)
    # print("\nCase 7 - Whitespace Handling:\n", node_7.to_html())

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
