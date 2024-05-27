import re
from textnode import (
    TextNode, 
    text_type_text, 
    text_type_image, 
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code
)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text_list = node.text.split(delimiter)
        if len(text_list) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for t in text_list:
            if len(t) == 0:
                continue
            if not t.startswith(" ") and not t.endswith(" "):
                new_nodes.append(TextNode(t, text_type))
            else:
                new_nodes.append(TextNode(t, text_type_text))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = r'!(.*?)(.*?\))'
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        extracted_image = extract_markdown_images(node.text)
        node_splited = re.split(pattern, node.text)
        for text in node_splited:
            if len(text) < 1:
                continue
            if text in [f'[{img_tup[0]}]({img_tup[1]})' for img_tup in extracted_image]:
                new_nodes.append(TextNode(re.findall(r"\[(.*?)\]", text)[0], text_type_image, re.findall(r"\((.*?)\)", text)[0]))
            else:
                new_nodes.append(TextNode(text, text_type_text))
    return new_nodes

        
def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r"(\[.*\[?\))"
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        extracted_links = extract_markdown_links(node.text)
        node_splited = re.split(pattern, node.text)
        for text in node_splited:
            if len(text) < 1:
                continue
            if text in [f'[{link_tup[0]}]({link_tup[1]})' for link_tup in extracted_links]:
                new_nodes.append(TextNode(re.findall(r"\[(.*?)\]", text)[0], text_type_link, re.findall(r"\((.*?)\)", text)[0]))
            else:
                new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)