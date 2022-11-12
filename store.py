import os
import sys
import shutil

if not os.path.isdir("stored"):
    os.mkdir("stored")

def input_name():
    name = input("Name your render: ")
    if os.path.isdir(os.path.join("stored", name)):
        print(f"Sorry, '{name}' already exists! Please choose another.")
        return input_name()
    else:
        return name

if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input_name()

storage_dir = os.path.join("stored", name)
assets = os.listdir("assets")

if "audio.mp3" in assets and "ascii.txt" in assets:
    os.mkdir(storage_dir)
    shutil.copy(os.path.join("assets", "audio.mp3"), storage_dir)
    shutil.copy(os.path.join("assets", "ascii.txt"), storage_dir)
    print(f"Stored render in '{storage_dir}'")

else:
    print("You must have audio and ASCII to store a render!")
