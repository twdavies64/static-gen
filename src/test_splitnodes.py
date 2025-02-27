import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
