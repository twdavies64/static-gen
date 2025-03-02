import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
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

    def test_some_more(self):
        md = """
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

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

    def test_some_more(self):
        # Test 2: Handles a markdown string with a heading, paragraph, and an unordered list
        # Ensures blocks are split correctly using blank lines
        md = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_leading_trailing_whitespace(self):
        # Test 3: Handles leading and trailing blank or newline characters
        # Ensures they are stripped correctly from each block
        md = """

        First block has leading space.

        Second block has trailing space.   

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["First block has leading space.", "Second block has trailing space."],
        )

    def test_strip_substrings(self):
        # Test 4: Handles removal of tabs and excessive spaces as specified
        # Blocks should have unwanted substrings removed (e.g., "\t", "    ")
        md = """\tBlock with a tab.

        Block with    multiple spaces in it."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Block with a tab.", "Block with multiple spaces in it."],
        )

    def test_empty_input(self):
        # Test 5: Handles cases with an empty input string
        # Should return an empty list since there's no content to split
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block_input(self):
        # Test 6: Handles markdown input with only one block (no blank lines)
        # Should return a single-item list containing the entire block
        md = """This is a single paragraph with no blank lines."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no blank lines."])

    def test_empty_lines_between_blocks(self):
        # Test 7: Handles multiple empty lines between blocks
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
        # Test 8: Handles a multiline list
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

    def test_newline_block_edge_case(self):
        # Test 9: Handles input where a block is purely a single newline
        # Ensures that such blocks are ignored and do not appear in the output
        md = """

        \n

        Valid block detected here.

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Valid block detected here."],
        )

    def test_code_block(self):
        # Test 10: Handles a block containing backticks for a code snippet
        # Ensures code blocks are preserved without alteration
        md = """
        ```python
        def hello_world():
            print("Hello, world!")
        ```

        Next block here.
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                '```python\ndef hello_world():\n    print("Hello, world!")\n```',
                "Next block here.",
            ],
        )

    def test_long_text_block(self):
        # Test 11: Handles a single block containing a very long paragraph
        # Ensures large chunks remain intact without splitting within the block
        md = """This is a very long paragraph that goes on and on without any blank lines to split it into blocks. It should remain as one single block, regardless of its length."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a very long paragraph that goes on and on without any blank lines to split it into blocks. It should remain as one single block, regardless of its length."
            ],
        )
