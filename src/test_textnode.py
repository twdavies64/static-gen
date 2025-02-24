import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
