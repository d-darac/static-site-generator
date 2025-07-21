import os
from website import copy_static, generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    try:
        copy_static(dir_path_static, dir_path_public)
        generate_page(
            os.path.join(dir_path_content, "index.md"),
            template_path,
            os.path.join(dir_path_public, "index.html"),
        )
    except Exception as e:
        print(e)


main()
