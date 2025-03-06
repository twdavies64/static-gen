import unittest

from blocknode import BlockType, block_to_block_type
from blocknode import markdown_to_html_node


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "# Single hash heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "###### Six hash heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\nprint('Hello World')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "```\nMultiple\nLines\nOf\nCode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "> Line one\n> Line two\n> Line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is a regular paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "This is a paragraph\nwith multiple\nlines of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # This test is kept because it aligns with the assignment requirements
    # about ordered lists starting with 1 and incrementing
    def test_invalid_markdown_formats(self):
        # Test that headings need a space after the #
        block = "#This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test that lists need a space after the - or number
        block = "-Not an unordered list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "1.Not an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test that ordered lists must start with 1 (per assignment requirement)
        block = "2. Should start with 1"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test that ordered lists must be sequential (per assignment requirement)
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_and_whitespace_blocks(self):
        # Test empty string
        block = ""
        self.assertEqual(block_to_block_type(block), None)

        # Test string with only spaces
        block = "   "
        self.assertEqual(block_to_block_type(block), None)

        # Test string with only newlines
        block = "\n\n\n"
        self.assertEqual(block_to_block_type(block), None)

        # Test string with mixed whitespace
        block = "  \n  \n  "
        self.assertEqual(block_to_block_type(block), None)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_unordered_list(self):
        md = """
    - This is a list item
    - This is another list item with **bold** text
    - And a third one with `code` in it
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list item</li><li>This is another list item with <b>bold</b> text</li><li>And a third one with <code>code</code> in it</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. First item
    2. Second item with _italic_ text
    3. Third item with **bold** text and `code`
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i> text</li><li>Third item with <b>bold</b> text and <code>code</code></li></ol></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
    # Main Heading

    Some paragraph text.

    ### Level 3 subheading with **bold**

    More text here.
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><p>Some paragraph text.</p><h3>Level 3 subheading with <b>bold</b></h3><p>More text here.</p></div>",
        )

    def test_blockquote(self):
        md = """
    > This is a blockquote
    > with multiple lines
    > and some **bold** and _italic_ text
    > and even some `code` too
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines and some <b>bold</b> and <i>italic</i> text and even some <code>code</code> too</blockquote></div>",
        )

    def test_empty_document(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p></p></div>")

    def test_multiple_heading_levels(self):
        md = """
    # H1 Heading
    ## H2 Heading
    ### H3 Heading
    #### H4 Heading
    ##### H5 Heading
    ###### H6 Heading
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1 Heading</h1><h2>H2 Heading</h2><h3>H3 Heading</h3><h4>H4 Heading</h4><h5>H5 Heading</h5><h6>H6 Heading</h6></div>",
        )

    def test_mixed_content(self):
        md = """
    # Document Title

    > Important quote
    > with formatting in **bold**

    Regular paragraph.

    ```
    code block
    with multiple lines
    ```

    - List item 1
    - List item 2
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Document Title</h1><blockquote>Important quote with formatting in <b>bold</b></blockquote><p>Regular paragraph.</p><pre><code>code block\nwith multiple lines\n</code></pre><ul><li>List item 1</li><li>List item 2</li></ul></div>",
        )

    def test_nested_inline_elements(self):
        md = """
    This is a paragraph with **bold text that contains `code` and _italic_ parts** inside it.
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph with <b>bold text that contains <code>code</code> and <i>italic</i> parts</b> inside it.</p></div>",
        )

    def test_consecutive_same_blocks(self):
        md = """
    # First Heading

    # Second Heading

    > First quote

    > Second quote
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>First Heading</h1><h1>Second Heading</h1><blockquote>First quote</blockquote><blockquote>Second quote</blockquote></div>",
        )

    def test_whitespace_handling(self):
        md = """
    
    # Heading with spaces

    
    Paragraph with   multiple   spaces   and

    newlines
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading with spaces</h1><p>Paragraph with multiple spaces and newlines</p></div>",
        )

    def test_inline_only(self):
        md = "This is **bold** and _italic_ and `code` without block containers."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bold</b> and <i>italic</i> and <code>code</code> without block containers.</p></div>",
        )

    def test_multiple_breaks(self):
        md = """
    First paragraph.


    
    Second paragraph after many breaks.
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph.</p><p>Second paragraph after many breaks.</p></div>",
        )

    # Added test for minimal blocks with content
    def test_minimal_blocks(self):
        md = """
    # Minimal heading

    > Minimal blockquote

    ```
    Minimal code block
    ```

    - Minimal list item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Minimal heading</h1><blockquote>Minimal blockquote</blockquote><pre><code>Minimal code block\n</code></pre><ul><li>Minimal list item</li></ul></div>",
        )

    # Added test for properly formatted ordered list
    def test_valid_ordered_list(self):
        md = """
    1. First item
    2. Second item
    3. Third item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )
