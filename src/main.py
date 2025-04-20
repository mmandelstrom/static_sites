from textnode import TextNode, TextType
import os, shutil
from markdown_to_html import markdown_to_html_node, extract_title
from generate_page import *

def main():
    static_root = "./static/"
    public_root = "./public/"
    clear_public(public_root)
    copy_static(static_root, public_root)
    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()