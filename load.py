from reset import reset_files
import os
import sys
import shutil

if not os.path.isdir("stored"):
    os.mkdir("stored")

def input_name():
    name = input("Load what render?: ")
    if os.path.isdir(os.path.join("stored", name)):
        return name
    else:
        print(f"'{name}' already exists!")

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Load what render?: ")

storage_dir = os.path.join("stored", name)

if os.path.isfile(os.path.join(storage_dir, "audio.mp3")) and os.path.isfile(os.path.join(storage_dir, "ascii.txt")):
    choice = input("Would you like to overwrite the current files? [y/N]: ").lower()

    if choice in ["yes", "y"]:
        reset_files()
        shutil.copy(os.path.join(storage_dir, "audio.mp3"), "assets")
        shutil.copy(os.path.join(storage_dir, "ascii.txt"), "assets")
        print(f"Loaded render from '{storage_dir}'")

    else:
        print("Ok, cancelled.")
    
else:
    print("Render not found!")
