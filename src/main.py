from textnode import TextNode, TextType
import os, shutil, sys
from markdown_to_html import markdown_to_html_node, extract_title
from generate_page import *

def main():
    if sys.argv[0]:
        basepath = sys.argv[0]
    else:
        basepath = "/"

    print(sys.argv[0])
    static_root = "./static/"
    public_root = "./docs/"
    clear_public(public_root)
    copy_static(static_root, public_root)
    generate_pages_recursive("./content/", "./template.html", public_root, basepath)
   
main()