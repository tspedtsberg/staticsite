from textnode import TextNode
from textnode import TextType
from markdown import split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

import shutil
import os

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static/"
dir_path_public = "./public/"
dir_path_content = "./content/"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)
        
    

if __name__ == "__main__":
    main()