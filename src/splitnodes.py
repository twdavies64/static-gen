from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for node in old_nodes:
        count = 0
        length = len(delimiter)
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        start = node.text.find(delimiter)
        end = node.text.find(delimiter, start + length)
        if start == -1 and end == -1:
            new_nodes.append(node)
            continue
        if start != -1 and end == -1:
            raise Exception("Invalid Markdown Syntax")
        if node.text.find(delimiter, end + length) != -1:
            raise Exception("wrong number of delimiters")
        if start > 0:
            new_nodes.append(TextNode(node.text[:start], node.text_type))
        middle = node.text[(start + length) : end]
        if text_type != TextType.CODE and middle.strip() == "":
            middle = ""
        new_nodes.append(TextNode(middle, text_type))
        if end + length < len(node.text):
            new_nodes.append(TextNode(node.text[(end + length) :], node.text_type))
    return new_nodes
