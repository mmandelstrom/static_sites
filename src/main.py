from textnode import TextNode, TextType
import os, shutil

def main():
    static_root = "./static/"
    public_root = "./public/"

    def clear_public(folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(f"Creating directory: {folder}")
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleting file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleting folder: {file_path}")

            except Exception as e:
                print(f'Could not remove {file_path}. Error: {e}')
   


    def copy_static(source, destination):
        if not os.path.exists(destination):
            os.mkdir(destination)
            print(f"Creating directory: {destination}")
        for filename in os.listdir(source):
            source_path = os.path.join(source, filename)
            destination_path = os.path.join(destination, filename)
            if os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)
                print(f"Copying {source_path} to {destination_path}")
            elif os.path.isdir(source_path):
                if not os.path.exists(destination_path):
                    os.mkdir(destination_path)
                    print(f"Creating directory: {destination_path}")
                copy_static(source_path, destination_path)
                    


    clear_public(public_root)
    copy_static(static_root, public_root)

main()