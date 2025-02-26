import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):  # 2 node objects are equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):  # 2 node objects are not equal
        node = TextNode("This node is awesome", TextType.IMAGE, url="http://xyz.com")
        node2 = TextNode("This node is special", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_eq(self):  # 2 node texts are equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, node2.text)

    def test_text_ne(self):  # 2 node texts are not equal
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is still a text node", TextType.CODE)
        self.assertNotEqual(node.text, node2.text)

    def test_text_type_eq(self):  # 2 node TextType objects are equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, node2.text_type)

    def test_text_type_ne(self):  # 2 node TextType objects are not equal
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is still a text node", TextType.IMAGE)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_url_is_none(self):  # url is None
        node = TextNode("This node is special", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_url_is_not_none(self):  # url is not None
        node = TextNode("This node is awesome", TextType.IMAGE, url="http://xyz.com")
        self.assertIsNotNone(node.url)

    def test_url_eq(self):  # node url is equal
        node = TextNode("This node is awesome", TextType.IMAGE, url="http://xyz.com")
        node2 = TextNode("This node is awesome", TextType.IMAGE, url="http://xyz.com")
        self.assertEqual(node.url, node2.url)

    def test_url_ne(self):  # node url is not equal
        node = TextNode("This node is awesome", TextType.IMAGE, url="http://xyz.com")
        node2 = TextNode(
            "This node is awesome", TextType.IMAGE, url="http://bootdev.com"
        )
        self.assertNotEqual(node.url, node2.url)

    def test_only_url_differs(self):
        node = TextNode("Same text", TextType.LINK, url="http://xyz.com")
        node2 = TextNode("Same text", TextType.LINK, url="http://abc.com")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="http://xyz.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "http://xyz.com"})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="http://xyz.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "http://xyz.com", "alt": "This is a text node"}
        )

    def test_invalid_text_type(self):
        with self.assertRaises(Exception) as context:
            node = TextNode(
                "This is a text node", "TextType.TEXT"
            )  # pass string instead of valid TextType
            html_node = text_node_to_html_node(node)
        self.assertTrue("Not a valid TextType for node" in str(context.exception))

    def test_missing_link(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is a text node", TextType.LINK)
            html_node = text_node_to_html_node(node)
        self.assertTrue("A link type requires a url" in str(context.exception))

    def test_missing_image(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is a text node", TextType.IMAGE)
            html_node = text_node_to_html_node(node)
        self.assertTrue("An image type requires a url" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
