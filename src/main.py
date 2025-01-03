from textnode import TextNode
from textnode import TextType
from markdown import split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
import shutil
import os
from copystatic import copy_files_recursive

dir_path_static = "./static/"
dir_path_public = "./public/"


def main():
    #deleting public folder
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print(f"copying static files to public folder")
    copy_files_recursive(dir_path_static, dir_path_public)

        
    

if __name__ == "__main__":
    main()