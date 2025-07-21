import os
import shutil
import re

from block_markdown import markdown_to_html_node


def copy_static(source, destination):
    source_path = os.path.realpath(os.path.join(".", source))
    destination_path = os.path.realpath(os.path.join(".", destination))

    if not os.path.exists(source):
        raise Exception(f"Source path not found: {source}")

    print(f"Deleting {destination} directory...")

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)

    print(f"Copying static files to {destination} directory...")
    copy_contents(source_path, destination_path)


def copy_contents(source_path, destination_path):
    os.mkdir(destination_path)
    source_contents = os.listdir(source_path)

    for item in source_contents:
        source_child_path = os.path.join(source_path, item)
        destination_child_path = os.path.join(destination_path, item)

        if os.path.isfile(source_child_path):
            print("Copying:", source_child_path, "\nto:     ", destination_child_path)
            shutil.copy(source_child_path, destination_child_path)
            continue

        copy_contents(source_child_path, destination_child_path)


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line.replace("#", "").strip()

    raise ValueError("No h1 headers found in markdown file.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(os.path.realpath(os.path.join(".", from_path)), "r")
    markdown = markdown_file.read()
    markdown_file.close()

    template_file = open(os.path.realpath(os.path.join(".", template_path)), "r")
    template = template_file.read()
    template_file.close()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = re.sub(r"{{\s*Title\s*}}", title, template)
    template = re.sub(r"{{\s*Content\s*}}", content, template)

    dest_dir = os.path.dirname(os.path.realpath(os.path.join(".", dest_path)))

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    html_file = open(os.path.realpath(os.path.join(".", dest_path)), "x")
    html_file.write(template)
    html_file.close()


"""
source/
    stuff/
        stuff.html
    thangs/
        thangs.html
    stuff_and_thangs.html


public/
"""
