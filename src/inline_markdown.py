from textnode import TextNode, text_type_text


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