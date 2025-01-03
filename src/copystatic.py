import os
import shutil

def copy_files_recursive(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for filename in os.listdir(source_dir):
        from_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        print(f" copying {from_path} -> {dest_path}")
        #check if its a file. If its a file copy it. 
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
            #if not a file, it will run the recursive func on the new path.
        else:
            copy_files_recursive(from_path, dest_path)

