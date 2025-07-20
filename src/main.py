from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


def main():
    nodes = text_to_textnodes(
        "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    )
    for node in nodes:
        print(node)


main()
