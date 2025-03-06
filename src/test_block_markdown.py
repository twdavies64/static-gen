import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Test 1: Handles a markdown string with bolded, italic, and code formatting
        # Spans across multiple lines and paragraphs, should split blocks correctly
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_whitespace_handling(self):
        # Test 2: Tests handling of various types of whitespace (spaces, tabs, newlines)
        # Ensures leading/trailing whitespace is stripped while preserving internal formatting
        md = """

        First block has leading space.

        Second block has trailing space.   

        \tBlock with a tab.

        Block with    multiple spaces in it.
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block has leading space.",
                "Second block has trailing space.",
                "Block with a tab.",
                "Block with    multiple spaces in it.",
            ],
        )

    def test_empty_input(self):
        # Test 3: Handles cases with an empty input string
        # Should return an empty list since there's no content to split
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block_input(self):
        # Test 4: Handles markdown input with only one block (no blank lines)
        # Should return a single-item list containing the entire block
        md = """This is a single paragraph with no blank lines."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no blank lines."])

    def test_empty_lines_between_blocks(self):
        # Test 5: Handles multiple empty lines between blocks
        # Ensures excessive newlines are ignored and blocks are split correctly
        md = """Block one.



        Block two.
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Block one.", "Block two."],
        )

    def test_multiline_list_block(self):
        # Test 6: Handles a multiline list
        # Ensures that all lines of a single list are combined into one block
        md = """
        - This is the first list item
        - This is the second list item
        - This is the third list item
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is the first list item\n- This is the second list item\n- This is the third list item"
            ],
        )

    # 7. Empty String as Input (Edge Case)
    def test_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # 8. Markdown with Excessive Consecutive Blank Lines
    def test_excessive_blank_lines(self):
        md = """Line one


    Line two"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line one", "Line two"])

    # 9. Blocks with Only Whitespace
    def test_empty_blocks_with_whitespace(self):
        md = """
        
    Block

        


    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block"])

    # 10. Multiline Blocks with Inconsistent Leading Spaces
    def test_multiline_blocks_with_leading_spaces(self):
        md = """- List item 1
    - Indented list item
    - Another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["- List item 1\n- Indented list item\n- Another list item"]
        )
