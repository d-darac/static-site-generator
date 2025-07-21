from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType
from website import copy_static


def main():
    try:
        copy_static("static", "public")
    except Exception as e:
        print(e)


main()
