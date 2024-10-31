import os
import shutil

def main():
    source = "./static/"
    destination = "./public/"

    def copy_static(source, destination, delete = True):
        #Delete everthing in public directory to ensure clean copies
        if delete:
            if os.path.isdir(destination):
                for item in os.listdir(destination):
                    item_path = os.path.join(destination, item)

                    try:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.remove(item_path)
                    
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)

                    except Exception as e:
                        print(f"Failed to delete {item_path}. Reason: {e}")

        #Check wether directory exist in destination, if not create it
        if not os.path.exists(destination):
            os.makedirs(destination)

        #Check if source is a directory
        if os.path.isdir(source):

        #loop through each item in the directory, if it is a file or link copy it   
            for item in os.listdir(source):
                source_path = os.path.join(source, item)
                destination_path = os.path.join(destination, item)
        
                if os.path.isfile(source_path) or os.path.islink(source_path):
                    print(f"Copying {source_path} to {destination_path}")
                    shutil.copy(source_path, destination_path)

        #if it is a directory recursively call function to copy contents    
                elif os.path.isdir(source_path):
                    copy_static(source_path, destination_path, delete = False)


                
   
main()