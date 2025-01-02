from textnode import TextNode
from textnode import TextType
from markdown import split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
import shutil
import os

def main():
#Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
#It should first delete all the contents of the destination directory to ensure that the copy is clean.
#It should copy all files and subdirectories, nested files, etc.
#I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.
    file_to_copy = './static/tester.py'
    destination_dir = "./public/"
    shutil.copy2(file_to_copy, destination_dir)
    

    return True
        
    

if __name__ == "__main__":
    main()