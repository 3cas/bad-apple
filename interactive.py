import os
import json

def prompt(message: str, *options):
    print(message)
    
    for option in options: 
        print(f"\t[{options.index(option) + 1}] {option}")

    user_input = input("Select an option: ")

    try:
        choice = int(user_input)
    except:
        for option in options:
            if user_input in option:
                choice = options.index(option) + 1
                break

    print()
    return choice

if not os.path.isfile("config.json"):
    # do not change these, instead change them in config.json which gets generated
    default_options = {
        "url": "https://www.youtube.com/watch?v=FtutLA63Cp8",
        "video_name": "video.webm",
        "framerate": 30,
        "color": True,
        "quiet": False,
        "skip_setup": False,
        "auto_reset": False,
        "delete_frames": False,
        "shading": [" ", ".", ":", "=", "#"]
    }

    with open("config.json", "w") as f:
        json.dump(default_options, f, indent=4)

    print("Generated config file!")

with open("config.json", "r") as f:
    config = json.load(f)

def config_option(display_name, setting_name = None):
    if not setting_name: setting_name = display_name.lower()
    return f"{display_name}: {config[setting_name]}"

def edit_config():
    ch = prompt(
        "Editing config file",
        config_option("Default video URL", "url"),
        config_option("Framerate"),
        "shading",
        ""
    )

def main():
    ch = prompt(
        "Welcome to the Bad Apple!! renderer. Please select an option.",
        "Generate ASCII",
        "Play generated ASCII",
        "Save generated ASCII",
        "Change settings",
        "Quit"
    )

    if ch == 1:
        pass

    elif ch == 2:
        pass

    elif ch == 3:
        pass

    elif ch == 4:
        pass

    elif ch == 5:
        print("Goodbye")

    else:
        print("Invalid option. Try again.")
        main()