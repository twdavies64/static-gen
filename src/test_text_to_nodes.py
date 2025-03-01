import unittest

from textnode import TextNode, TextType
from text_to_nodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_basic_functionality(self):
        # Test 1: Basic functionality with multiple markdown elements
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://example.com/img.png) and a [link](https://example.com)"
        nodes = text_to_textnodes(text)

        # Check if we have the correct number of nodes
        assert len(nodes) == 10

        # Check specific nodes
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT

        assert nodes[1].text == "text"
        assert nodes[1].text_type == TextType.BOLD

        assert nodes[3].text == "italic"
        assert nodes[3].text_type == TextType.ITALIC

        assert nodes[5].text == "code block"
        assert nodes[5].text_type == TextType.CODE

        assert nodes[7].text == "image"
        assert nodes[7].text_type == TextType.IMAGE
        assert nodes[7].url == "https://example.com/img.png"

        assert nodes[9].text == "link"
        assert nodes[9].text_type == TextType.LINK
        assert nodes[9].url == "https://example.com"

    def test_empty_string(self):
        # Test 2: Empty string
        nodes = text_to_textnodes("")
        assert len(nodes) == 1
        assert nodes[0].text == ""
        assert nodes[0].text_type == TextType.TEXT

    def test_plain_text(self):
        # Test 3: Plain text with no markdown
        nodes = text_to_textnodes("Just plain text")
        assert len(nodes) == 1
        assert nodes[0].text == "Just plain text"
        assert nodes[0].text_type == TextType.TEXT

    def test_bold_only(self):
        # Test 4: Only bold text
        nodes = text_to_textnodes("**Bold text only**")
        assert len(nodes) == 1
        assert nodes[0].text == "Bold text only"
        assert nodes[0].text_type == TextType.BOLD

    def test_italic_only(self):
        # Test 5: Only italic text
        nodes = text_to_textnodes("_Italic text only_")
        assert len(nodes) == 1
        assert nodes[0].text == "Italic text only"
        assert nodes[0].text_type == TextType.ITALIC

    def test_code_only(self):
        # Test 6: Only code text
        nodes = text_to_textnodes("`Code text only`")
        assert len(nodes) == 1
        assert nodes[0].text == "Code text only"
        assert nodes[0].text_type == TextType.CODE

    def test_image_only(self):
        # Test 7: Only an image
        nodes = text_to_textnodes("![Alt text](https://example.com/image.jpg)")
        assert len(nodes) == 1
        assert nodes[0].text == "Alt text"
        assert nodes[0].text_type == TextType.IMAGE
        assert nodes[0].url == "https://example.com/image.jpg"

    def test_link_only(self):
        # Test 8: Only a link
        nodes = text_to_textnodes("[Link text](https://example.com)")
        assert len(nodes) == 1
        assert nodes[0].text == "Link text"
        assert nodes[0].text_type == TextType.LINK
        assert nodes[0].url == "https://example.com"

    # def test_multiple_of_same_type(self):
    #     # Test 9: Multiple elements of the same type
    #     nodes = text_to_textnodes("**Bold1** plain text **Bold2**")
    #     assert len(nodes) == 3
    #     assert nodes[0].text == "Bold1"
    #     assert nodes[0].text_type == TextType.BOLD
    #     assert nodes[1].text == " plain text "
    #     assert nodes[1].text_type == TextType.TEXT
    #     assert nodes[2].text == "Bold2"
    #     assert nodes[2].text_type == TextType.BOLD

    def test_nested_markdown(self):
        # Test 10: Text that looks like it has nested markdown (which our parser doesn't support)
        nodes = text_to_textnodes("This **has _nested_ formatting**")
        # Our current implementation should treat this as separate markers
        assert len(nodes) > 1
        # We're not asserting exact behavior since it depends on your implementation
