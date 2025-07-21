import os
import shutil
import re

from block_markdown import markdown_to_html_node


def copy_static(source, destination):
    if not os.path.exists(source):
        raise Exception(f"Source path not found: {source}")

    print(f"Deleting {destination} directory...")

    if os.path.exists(destination):
        shutil.rmtree(destination)

    print(f"Copying static files to {destination} directory...")
    copy_contents(source, destination)


def copy_contents(src_dir_path, dest_dir_path):
    os.mkdir(dest_dir_path)
    src_contents = os.listdir(src_dir_path)

    for item in src_contents:
        src_child_path = os.path.join(src_dir_path, item)
        dest_child_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_child_path):
            print("Copying:", src_child_path, "\nto:     ", dest_child_path)
            shutil.copy(src_child_path, dest_child_path)
            continue

        copy_contents(src_child_path, dest_child_path)


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line.replace("#", "").strip()

    raise ValueError("No h1 headers found in markdown file.")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = re.sub(r"{{\s*Title\s*}}", title, template)
    template = re.sub(r"{{\s*Content\s*}}", content, template)
    template = re.sub(r'href="\/', f'href="{basepath}', template)
    template = re.sub(r'src="\/', f'src="{basepath}', template)

    dest_dir = os.path.dirname(dest_path)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    html_file = open(dest_path, "x")
    html_file.write(template)
    html_file.close()


def generate_pages_recursive(src_dir_path, template_path, dest_dir_path, basepath):
    src_contents = os.listdir(src_dir_path)

    for item in src_contents:
        src_child_path = os.path.join(src_dir_path, item)
        dest_child_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_child_path):
            if src_child_path.endswith(".md"):
                generate_page(
                    src_child_path,
                    template_path,
                    dest_child_path.replace("md", "html"),
                    basepath,
                )
            continue

        generate_pages_recursive(
            src_child_path, template_path, dest_child_path, basepath
        )


"""
source/
    stuff/
        stuff.html
    thangs/
        thangs.html
    stuff_and_thangs.html


public/
"""
