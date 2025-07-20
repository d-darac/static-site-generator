import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    CODE = "code"
    HEADING = "heading"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue

        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.CODE:
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("invalid code block")
                text = block[4:-3]
                raw_text_node = TextNode(text, TextType.TEXT)
                child = text_node_to_html_node(raw_text_node)
                code = ParentNode("code", [child])
                nodes.append(ParentNode("pre", [code]))

            case BlockType.HEADING:
                lines = block.split("\n")
                for line in lines:
                    header_level = line.count("#")
                    children = text_to_children(line.replace("#", "").strip())
                    nodes.append(ParentNode(f"h{header_level}", children))

            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                elements = []
                for item in items:
                    text = item[3:]
                    children = text_to_children(text)
                    elements.append(ParentNode("li", children))

                nodes.append(ParentNode("ol", elements))

            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    new_lines.append(line.lstrip(">").strip())
                content = " ".join(new_lines)
                children = text_to_children(content)
                nodes.append(ParentNode("blockquote", children))

            case BlockType.PARAGRAPH:
                children = text_to_children(block.replace("\n", " "))
                nodes.append(ParentNode("p", children))

            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                elements = []
                for item in items:
                    text = item[2:]
                    children = text_to_children(text)
                    elements.append(ParentNode("li", children))

                nodes.append(ParentNode("ul", elements))

            case _:
                raise ValueError("invalid block type")

    return ParentNode("div", nodes)


def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes
