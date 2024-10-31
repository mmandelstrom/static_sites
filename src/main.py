import os
import shutil
from copy_static import *
from generate_page import *

def main():

    source = "./static/"
    destination = "./public/"
    copy_static(source, destination)

    generate_page("./static/content/index.md", "./template.html", "./public/index.html")

    
   
main()