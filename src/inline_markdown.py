import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    # Find potential image markdown patterns
    potential_matches = re.finditer(r"!\[(.*?)\]\(", text)

    results = []
    for match in potential_matches:
        alt_text = match.group(1)
        start_idx = match.end()

        # Count parentheses to find the matching closing one
        paren_count = 1
        for i in range(start_idx, len(text)):
            if text[i] == "(":
                paren_count += 1
            elif text[i] == ")":
                paren_count -= 1

            if paren_count == 0:
                results.append((alt_text, text[start_idx:i]))
                break

    return results


def extract_markdown_links(text):
    # Find potential link markdown patterns
    potential_matches = re.finditer(r"(?<!!)\[(.*?)\]\(", text)

    results = []
    for match in potential_matches:
        link_text = match.group(1)
        start_idx = match.end()

        # Count parentheses to find the matching closing one
        paren_count = 1
        for i in range(start_idx, len(text)):
            if text[i] == "(":
                paren_count += 1
            elif text[i] == ")":
                paren_count -= 1

            if paren_count == 0:
                results.append((link_text, text[start_idx:i]))
                break

    return results


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        current_text = node.text
        for text, link in images:
            link_marker = f"![{text}]({link})"
            sections = current_text.split(link_marker, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.IMAGE, link))
            if len(sections) > 1:
                current_text = sections[1]
            else:
                current_text = ""

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        current_text = node.text
        for alt, link in links:
            link_marker = f"[{alt}]({link})"
            sections = current_text.split(link_marker, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            if len(sections) > 1:
                current_text = sections[1]
            else:
                current_text = ""

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes
