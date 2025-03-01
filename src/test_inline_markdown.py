import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodes(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with some **very bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with some ", TextType.TEXT),
                TextNode("very bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_no_delimiter(self):
        with self.assertRaises(Exception) as context:
            # No delimiters
            node = TextNode("plain text", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "", TextType.ITALIC)
        self.assertTrue("wrong number of delimiters" in str(context.exception))

    def test_too_many_delim(self):
        with self.assertRaises(Exception) as context:
            # Too many delimiters
            node = TextNode("**one** **two**", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "", TextType.ITALIC)
        self.assertTrue("wrong number of delimiters" in str(context.exception))

    def test_split_nodes_delimiter(self):
        # Test 1: No delimiters - should keep text as-is
        node1 = TextNode("Hello world", TextType.TEXT)
        new_nodes1 = split_nodes_delimiter([node1], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes1), 1)
        self.assertEqual(new_nodes1[0].text, "Hello world")
        self.assertEqual(new_nodes1[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_valid_pair(self):
        # Test 2: Valid delimiters - should split into three nodes
        node2 = TextNode("Hello *world* today", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes2), 3)
        self.assertEqual(new_nodes2[0].text, "Hello ")
        self.assertEqual(new_nodes2[1].text, "world")
        self.assertEqual(new_nodes2[2].text, " today")
        self.assertEqual(new_nodes2[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes2[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes2[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_single_delimiter(self):
        # Test 3: Single delimiter - should raise exception
        node3 = TextNode("Hello *world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node3], "*", TextType.ITALIC)

    def test_split_nodes_delimiter_non_text(self):
        # Test 4: Non-text node - should remain unchanged
        node4 = TextNode("Hello *world*", TextType.BOLD)
        new_nodes4 = split_nodes_delimiter([node4], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes4), 1)
        self.assertEqual(new_nodes4[0].text, "Hello *world*")
        self.assertEqual(new_nodes4[0].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_multiple_pairs(self):
        # Test 5: Multiple delimited sections - should raise exception
        node5 = TextNode("Hello *world* *today*", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node5], "*", TextType.ITALIC)

    def test_split_nodes_delimiter_multiple_nodes(self):
        # Test 6: Multiple nodes input
        node6a = TextNode("Hello ", TextType.TEXT)
        node6b = TextNode("*world*", TextType.BOLD)
        node6c = TextNode(" today", TextType.TEXT)
        new_nodes6 = split_nodes_delimiter(
            [node6a, node6b, node6c], "*", TextType.ITALIC
        )
        self.assertEqual(len(new_nodes6), 3)
        self.assertEqual(new_nodes6[0].text, "Hello ")
        self.assertEqual(new_nodes6[1].text, "*world*")  # Bold node stays unchanged
        self.assertEqual(new_nodes6[2].text, " today")

    def test_different_delimiters(self):
        # Test 7: Different delimiter types

        # Bold test
        node1 = TextNode("Hello **world** today", TextType.TEXT)
        new_nodes1 = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes1), 3)
        self.assertEqual(new_nodes1[1].text_type, TextType.BOLD)

        # Code test
        node2 = TextNode("Hello `world` today", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes2), 3)
        self.assertEqual(new_nodes2[1].text_type, TextType.CODE)

    def test_empty_and_whitespace(self):
        # Test 8: Empty and whitespace between delimiters

        # Empty delimiter content
        node1 = TextNode("Hello ** ** today", TextType.TEXT)
        new_nodes1 = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes1), 3)
        self.assertEqual(new_nodes1[1].text, "")

        # Whitespace delimiter content
        node2 = TextNode("Hello `   ` today", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes2), 3)
        self.assertEqual(new_nodes2[1].text, "   ")

    def test_edge_cases(self):
        # Test 9: Edge cases

        # Delimiter at start
        node1 = TextNode("**bold** text", TextType.TEXT)
        new_nodes1 = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes1), 2)
        self.assertEqual(new_nodes1[0].text, "bold")
        self.assertEqual(new_nodes1[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes1[1].text, " text")

        # Delimiter at end
        node2 = TextNode("text **bold**", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes2), 2)
        self.assertEqual(new_nodes2[0].text, "text ")
        self.assertEqual(new_nodes2[1].text, "bold")
        self.assertEqual(new_nodes2[1].text_type, TextType.BOLD)

        # Just delimiters and content
        node3 = TextNode("**bold**", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes3), 1)
        self.assertEqual(new_nodes3[0].text, "bold")
        self.assertEqual(new_nodes3[0].text_type, TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    # Test 1: Basic case - single image extraction
    def test_extract_markdown_images_1_basic(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # Test 2: Multiple images in the same text
    def test_extract_markdown_images_2_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("second image", "https://i.imgur.com/3elNhQu.png"),
            ],
            matches,
        )

    # Test 3: No images in the text
    def test_extract_markdown_images_3_none(self):
        matches = extract_markdown_images("This text has no images")
        self.assertListEqual([], matches)

    # Test 4: Image with empty alt text
    def test_extract_markdown_images_4_empty_alt(self):
        matches = extract_markdown_images(
            "This is an image with no alt text: ![](https://example.com/image.jpg)"
        )
        self.assertListEqual([("", "https://example.com/image.jpg")], matches)

    # Test 5: Image with special characters in alt text and URL
    def test_extract_markdown_images_5_special_chars(self):
        matches = extract_markdown_images(
            "![Image with spaces and symbols!](https://example.com/image-with-dash.jpg)"
        )
        self.assertListEqual(
            [
                (
                    "Image with spaces and symbols!",
                    "https://example.com/image-with-dash.jpg",
                )
            ],
            matches,
        )

    # Test 6: Malformed image markdown - missing closing parenthesis
    def test_extract_markdown_images_6_malformed(self):
        matches = extract_markdown_images(
            "This is a malformed image syntax: ![alt](https://example.com/missing-parenthesis"
        )
        self.assertListEqual(
            [], matches
        )  # Should return empty list for malformed markdown

    # Test 7: Image with URL that contains parentheses
    def test_extract_markdown_images_7_nested_parentheses(self):
        matches = extract_markdown_images(
            "![alt text](https://example.com/image(1).jpg)"
        )
        self.assertListEqual(
            [("alt text", "https://example.com/image(1).jpg")], matches
        )

    # Test 8: Multiple identical images
    def test_extract_markdown_images_8_duplicate_images(self):
        matches = extract_markdown_images(
            "![same](https://example.com/same.jpg) and again ![same](https://example.com/same.jpg)"
        )
        self.assertListEqual(
            [
                ("same", "https://example.com/same.jpg"),
                ("same", "https://example.com/same.jpg"),
            ],
            matches,
        )

    # Test 9: Image with query parameters in URL
    def test_extract_markdown_images_9_url_with_params(self):
        matches = extract_markdown_images(
            "![queryparams](https://example.com/image.jpg?size=large&format=png)"
        )
        self.assertListEqual(
            [("queryparams", "https://example.com/image.jpg?size=large&format=png")],
            matches,
        )

    # Test 10: Image markdown directly adjacent to text
    def test_extract_markdown_images_10_adjacent_text(self):
        matches = extract_markdown_images(
            "Text![no space](https://example.com/nospace.jpg)more text"
        )
        self.assertListEqual([("no space", "https://example.com/nospace.jpg")], matches)

    # Test 11: Image followed immediately by another image
    def test_extract_markdown_images_11_adjacent_images(self):
        matches = extract_markdown_images(
            "![first](https://example.com/1.jpg)![second](https://example.com/2.jpg)"
        )
        self.assertListEqual(
            [
                ("first", "https://example.com/1.jpg"),
                ("second", "https://example.com/2.jpg"),
            ],
            matches,
        )

    # Test 12: Image with unusual URL protocol
    def test_extract_markdown_images_12_unusual_protocol(self):
        matches = extract_markdown_images("![ftp image](ftp://example.com/image.jpg)")
        self.assertListEqual([("ftp image", "ftp://example.com/image.jpg")], matches)

    # Test 13: Empty input string
    def test_extract_markdown_images_13_empty_input(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

        # Test 14: Image with no URL (malformed)

    def test_extract_markdown_images_14_no_url(self):
        matches = extract_markdown_images("![alt text]()")
        self.assertListEqual([("alt text", "")], matches)

    # Test 15: Regular link mistaken as image
    def test_extract_markdown_images_15_not_an_image(self):
        matches = extract_markdown_images(
            "This is just a regular [link](https://example.com), not an image"
        )
        self.assertListEqual([], matches)

    # Test 16: Image with whitespace in URL
    def test_extract_markdown_images_16_url_with_whitespace(self):
        matches = extract_markdown_images(
            "![alt](https://example.com/path with spaces.jpg)"
        )
        self.assertListEqual(
            [("alt", "https://example.com/path with spaces.jpg")], matches
        )

    # Test 17: Multiple lines with images
    def test_extract_markdown_images_17_multiline(self):
        matches = extract_markdown_images(
            "Line 1 with ![image1](https://example.com/1.jpg)\nLine 2 with ![image2](https://example.com/2.jpg)"
        )
        self.assertListEqual(
            [
                ("image1", "https://example.com/1.jpg"),
                ("image2", "https://example.com/2.jpg"),
            ],
            matches,
        )

    # Test 18: Image with escaped characters in alt text
    def test_extract_markdown_images_18_escaped_chars(self):
        matches = extract_markdown_images(
            "![alt with \\[brackets\\]](https://example.com/image.jpg)"
        )
        self.assertListEqual(
            [("alt with \\[brackets\\]", "https://example.com/image.jpg")], matches
        )


class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_wrong(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                    TextType.TEXT,
                )
            ],
            new_nodes,
        )

    # Test 1: Empty text node
    def test_split_image_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    # Test 2: Node with no images
    def test_split_image_no_images(self):
        node = TextNode("This is text with no images at all", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    # Test 3: Image at the beginning of text
    def test_split_image_at_beginning(self):
        node = TextNode(
            "![start image](https://example.com/img.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test 4: Image at the end of text
    def test_split_image_at_end(self):
        node = TextNode(
            "Text followed by ![end image](https://example.com/end.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("end image", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    # Test 5: Multiple nodes as input
    def test_split_image_multiple_nodes(self):
        node1 = TextNode(
            "Text with ![image1](https://example.com/1.png)", TextType.TEXT
        )
        node2 = TextNode(
            "More text with ![image2](https://example.com/2.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("More text with ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    # Test 6: Multiple images with no text between them
    def test_split_image_adjacent(self):
        node = TextNode(
            "![image1](https://example.com/1.png)![image2](https://example.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("image2", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    # Test 7: Malformed image markdown (missing closing parenthesis)
    def test_split_image_malformed(self):
        node = TextNode(
            "This has a ![bad image](https://example.com/bad.png and ![good image](https://example.com/good.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Should only extract the properly formatted image
        self.assertListEqual(
            [
                TextNode(
                    "This has a ![bad image](https://example.com/bad.png and ",
                    TextType.TEXT,
                ),
                TextNode("good image", TextType.IMAGE, "https://example.com/good.png"),
            ],
            new_nodes,
        )

    # Test 8: Non-text node input
    def test_split_image_non_text_node(self):
        node = TextNode(
            "existing image", TextType.IMAGE, "https://example.com/existing.png"
        )
        new_nodes = split_nodes_image([node])
        # Non-TEXT nodes should be returned unchanged
        self.assertListEqual([node], new_nodes)

    # Test 9: Empty list input
    def test_split_image_empty_list(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual([], new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_link_wrong(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.TEXT,
                )
            ],
            new_nodes,
        )

    # Test 1: Empty text node
    def test_split_link_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    # Test 2: Node with no links
    def test_split_link_no_links(self):
        node = TextNode("This is text with no links at all", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    # Test 3: Link at the beginning of text
    def test_split_link_at_beginning(self):
        node = TextNode(
            "[start link](https://example.com/start) followed by text", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start link", TextType.LINK, "https://example.com/start"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test 4: Link at the end of text
    def test_split_link_at_end(self):
        node = TextNode(
            "Text followed by [end link](https://example.com/end)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("end link", TextType.LINK, "https://example.com/end"),
            ],
            new_nodes,
        )

    # Test 5: Multiple nodes as input
    def test_split_link_multiple_nodes(self):
        node1 = TextNode("Text with [link1](https://example.com/1)", TextType.TEXT)
        node2 = TextNode("More text with [link2](https://example.com/2)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode("More text with ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )

    # Test 6: Multiple links with no text between them
    def test_split_link_adjacent(self):
        node = TextNode(
            "[link1](https://example.com/1)[link2](https://example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )

    # Test 7: Malformed link markdown (missing closing parenthesis)
    def test_split_link_malformed(self):
        node = TextNode(
            "This has a [bad link](https://example.com/bad and [good link](https://example.com/good)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Should only extract the properly formatted link
        self.assertListEqual(
            [
                TextNode(
                    "This has a [bad link](https://example.com/bad and ", TextType.TEXT
                ),
                TextNode("good link", TextType.LINK, "https://example.com/good"),
            ],
            new_nodes,
        )

    # Test 8: Non-text node input
    def test_split_link_non_text_node(self):
        node = TextNode("existing link", TextType.LINK, "https://example.com/existing")
        new_nodes = split_nodes_link([node])
        # Non-TEXT nodes should be returned unchanged
        self.assertListEqual([node], new_nodes)

    # Test 9: Empty list input
    def test_split_link_empty_list(self):
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)

    # Test 10: Links with special characters
    def test_split_link_special_chars(self):
        node = TextNode(
            "Check out [this link with spaces](https://example.com/path with spaces) and [another-one](https://example.com/path-with-dashes)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode(
                    "this link with spaces",
                    TextType.LINK,
                    "https://example.com/path with spaces",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "another-one", TextType.LINK, "https://example.com/path-with-dashes"
                ),
            ],
            new_nodes,
        )

    # Test 11: Links with empty text
    def test_split_link_empty_text_content(self):
        node = TextNode("Before [](https://example.com/empty) after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com/empty"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test 12: Link immediately followed by another markdown element
    def test_split_link_followed_by_markdown(self):
        node = TextNode(
            "This is a [link](https://example.com)**bold text**", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("**bold text**", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
