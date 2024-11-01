import os
import shutil
from copy_static import *
from generate_page import *

def main():

    source = "./static/"
    destination = "./public/"
    copy_static(source, destination)

    generate_pages_recursive("./static/content/", "./template.html", "./public/")

    
   
main()