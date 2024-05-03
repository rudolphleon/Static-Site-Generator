from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

import re

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes  # This return statement ensures that a list is always returned


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        start = 0
        for image_tup in images:
            pos = text.find(f"![{image_tup[0]}]({image_tup[1]})", start)
            if pos > start:
                new_nodes.append(TextNode(text[start:pos], text_type_text))
            new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
            start = pos + len(f"![{image_tup[0]}]({image_tup[1]})")
        
        if start < len(text):
            new_nodes.append(TextNode(text[start:], text_type_text))
    return new_nodes  # Ensure this function always returns a list

         
    
def split_nodes_link(old_nodes):
    if not old_nodes:
        return []  # Early return to handle None or empty input
    
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        start = 0
        for link_tup in links:
            pos = text.find(f"[{link_tup[0]}]({link_tup[1]})", start)
            if pos > start:
                new_nodes.append(TextNode(text[start:pos], text_type_text))
            new_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
            start = pos + len(f"[{link_tup[0]}]({link_tup[1]})")
        
        if start < len(text):
            new_nodes.append(TextNode(text[start:], text_type_text))
    
    return new_nodes

    
def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
    nodes = split_nodes_delimiter(nodes, '`', text_type_code)
    nodes = [node for node in nodes if node.text.strip()]  # Remove empty nodes
    return nodes






    return new_nodes