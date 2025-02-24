import unittest

from htmlnode import HTMLNode


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
