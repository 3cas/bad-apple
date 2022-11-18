import os
import json

OPTION_INVALID = "Invalid option. Try again."
CAN_CANCEL = "You can leave the field blank to keep the setting unchanged."

CONFIG_FILE = "config.json"

def write_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

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

def ask_boolean(message: str):
    user_input = input(f"{message} [y/n, t/f]: ").lower()

    if user_input in ["true", "t", "yes", "y", "on", "1"]:
        return True
    elif user_input in ["false", "f", "no", "n", "off", "0"]:
        return False
    elif user_input == "":
        return "leave"

    else:   
        print("You must answer true or false!")
        ask_boolean(message)

def edit_config(resume = None):
    if resume:
        ch = resume
    else:
        ch = prompt(
            "\nEditing config file.",
            f"Default video path: {config['path']}",
            f"Framerate: {config['framerate']}",
            f"Shading on/off: {config['shade']}",
            "Shading levels...",
            f"Use ANSI colors: {config['color']}",
            f"Quiet output: {config['quiet']}",
            f"Delete frames after: {config['delete_frames']}",
            "Back"
        )

    if ch == 1:
        print(f"The default video path or URL is '{config['path']}'.")
        print(CAN_CANCEL)
        user_input = input("New path or URL: ")
        
        if user_input:
            config["path"] = user_input
            write_config()
            print(f"Video path has been set to '{config['path']}'")

    elif ch == 2:
        print(f"The framerate is set to {config['framerate']} FPS.")
        print(CAN_CANCEL)
        user_input = input("New framerate: ")

        if user_input:
            try:
                config["framerate"] = int(user_input)

            except:
                print("The framerate provided must be an integer!")
                edit_config(2)

            else:
                write_config()
                print(f"Framerate has been set to {config['framerate']}")

    elif ch == 3:
        print(f"Whether to use shading is set to {config['shade']}. If this is set to false, one character will be used for all shades (useful in conjunction with colors)")
        print(CAN_CANCEL)
        user_input = ask_boolean("Use shading?")

        if user_input == "leave":
            print()

    elif ch == 4:
        print("shading")

    elif ch == 5:
        print("color")

    elif ch == 6:
        print("quiet")

    elif ch == 7:
        print("delete")

    elif ch == 8:
        print("Exiting to main menu\n")
        return

    else:
        print(OPTION_INVALID)

    edit_config()

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
        print("generate")

    elif ch == 2:
        print("play")

    elif ch == 3:
        print("save")

    elif ch == 4:
        print("settings")

    elif ch == 5:
        print("Goodbye")

    else:
        print(OPTION_INVALID)
        main()

if __name__ == "__main__":
    if not os.path.isfile(CONFIG_FILE):
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

        with open(CONFIG_FILE, "w") as f:
            json.dump(default_options, f, indent=4)

        print("Generated config file!")

        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

    main()