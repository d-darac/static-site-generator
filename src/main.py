import sys
from website import copy_static, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    try:
        basepath = "/"
        args = sys.argv

        if len(args) > 1:
            if not args[1].startswith("--"):
                basepath = f"/{args[1]}/"

            if "--github-pages" in args[2:]:
                global dir_path_public
                dir_path_public = "./docs"

        copy_static(dir_path_static, dir_path_public)
        generate_pages_recursive(
            dir_path_content, template_path, dir_path_public, basepath
        )

    except Exception as e:
        print(e)


main()
