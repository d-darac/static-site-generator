import os
import shutil


def copy_static(source, destination):
    source_path = os.path.realpath(os.path.join(".", source))
    destination_path = os.path.realpath(os.path.join(".", destination))

    if not os.path.exists(source):
        raise Exception(f"Source path not found: {source}")

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)

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


"""
source/
    stuff/
        stuff.html
    thangs/
        thangs.html
    stuff_and_thangs.html


public/
"""
