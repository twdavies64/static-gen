import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_is_none(self):  # node elements are all None
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_is_not_none(self):  # node elements are not None
        node = HTMLNode("", "", ["", "", [], {}], {})
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.children)
        self.assertIsNotNone(node.props)

    # def test_eq(self):
    #     node = HTMLNode("", "", ["", "", [], {}], {})
    #     node2 = HTMLNode("", "", ["", "", [], {}], {})
    #     self.assertEqual(node, node2)

    def test_props_to_html(self):  # props are converted to html
        node = HTMLNode(
            "a",
            "blah blah blah blah",
            "",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(), f' href="https://www.google.com" target="_blank"'
        )

    def test_none_props(self):
        node = HTMLNode(
            "a",
            "blah blah blah blah",
            "",
        )
        self.assertEqual(node.props_to_html(), "")

    def test_single_prop(self):
        node = HTMLNode("a", "blah blah blah blah", "", {"class": "bold"})
        self.assertEqual(node.props_to_html(), f' class="bold"')

    def test_empty_props(self):
        node = HTMLNode("a", "blah blah blah blah", "", {})
        self.assertEqual(node.props_to_html(), "")

    def test_invalid_props_type(self):
        # Try to create HTMLNode with props as a list instead of dict
        with self.assertRaises(TypeError):
            HTMLNode(props=["not", "a", "dictionary"])


class TestLeafNode(unittest.TestCase):
    def test_a_tag(self):
        node = LeafNode("a", "Clicky clicky!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Clicky clicky!</a>'
        )

    def test_p_tag(self):
        node = LeafNode(
            "p", "This is a test of your local emergency radio broadcasting system"
        )
        self.assertEqual(
            node.to_html(),
            "<p>This is a test of your local emergency radio broadcasting system</p>",
        )

    def test_no_tag(self):
        node = LeafNode(None, "It's alyways just been text anyway")
        self.assertEqual(node.to_html(), "It's alyways just been text anyway")

    def test_no_val(self):
        node = LeafNode("img", None, {"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image" />')

    def test_invalid_props_type_leaf(self):
        # Try to create LeafNode with props as a string
        with self.assertRaises(TypeError):
            LeafNode("p", "text", props="not a dictionary")


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_nested_parent(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>",
        )

    def test_props(self):
        node = ParentNode("div", [LeafNode("span", "text")], {"class": "container"})
        self.assertEqual(
            node.to_html(), '<div class="container"><span>text</span></div>'
        )

    def test_no_children(self):
        with self.assertRaises(TypeError):
            ParentNode("p")

    def test_empty_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", [])
            node.to_html()

    def test_nested_with_props(self):
        node = ParentNode(
            "div",
            [ParentNode("p", [LeafNode("span", "text")], {"class": "paragraph"})],
            {"id": "container"},
        )
        self.assertEqual(
            node.to_html(),
            '<div id="container"><p class="paragraph"><span>text</span></p></div>',
        )

    def test_multiple_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container", "id": "main", "data-test": "test123"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main" data-test="test123"><p>Hello</p></div>',
        )

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("p", "text")])
            node.to_html()

    def test_none_props(self):
        node = ParentNode("div", [LeafNode("p", "text")], None)
        self.assertEqual(node.to_html(), "<div><p>text</p></div>")

    def test_mixed_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "text"),
                ParentNode("p", [LeafNode("b", "bold")]),
                LeafNode("i", "italic"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><span>text</span><p><b>bold</b></p><i>italic</i></div>",
        )

    def test_self_closing_children(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "text"), LeafNode("br", None), LeafNode("p", "more text")],
        )
        self.assertEqual(node.to_html(), "<div><p>text</p><br /><p>more text</p></div>")

    def test_invalid_children_type(self):
        with self.assertRaises(TypeError):
            ParentNode("div", "not a list")  # Passing string instead of list

    def test_invalid_props_type_parent(self):
        # Try to create ParentNode with props as a tuple
        with self.assertRaises(TypeError):
            ParentNode("div", [LeafNode("p", "text")], props=(1, 2, 3))

    def test_tag_required(self):
        with self.assertRaises(TypeError):
            ParentNode(children=[LeafNode("p", "text")])

    def test_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section", [ParentNode("article", [LeafNode("p", "Deep text")])]
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p>Deep text</p></article></section></div>",
        )

    def test_none_child_validation(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [None, None])  # List of only None values

    def test_mixed_none_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "First"),
                None,
                LeafNode("p", "Second"),
                None,
                LeafNode("p", "Third"),
            ],
        )
        # This test expects None children to be ignored/filtered out
        self.assertEqual(
            node.to_html(), "<div><p>First</p><p>Second</p><p>Third</p></div>"
        )

    def test_special_chars(self):
        node = ParentNode(
            "div", [LeafNode("p", "Hello")], {"data-special@": "test&<>\"'"}
        )
        self.assertEqual(
            node.to_html(), '<div data-special@="test&<>&quot;\'"><p>Hello</p></div>'
        )

    def test_quoted_props(self):
        node = ParentNode(
            "div", [LeafNode("p", "Hello")], {"data-text": 'He said "Hello!"'}
        )
        self.assertEqual(
            node.to_html(),
            '<div data-text="He said &quot;Hello!&quot;"><p>Hello</p></div>',
        )

    def test_many_children(self):
        children = [LeafNode("span", str(i)) for i in range(1000)]
        node = ParentNode("div", children)
        result = node.to_html()  # Should complete in reasonable time

    # def test_inner_outer_props(self):
    #     node = ParentNode(
    #         "div",
    #         [ParentNode("p", [LeafNode("b", "text")])],
    #         {"class": "outer"}
    #     )
    #     print(node.to_html())
