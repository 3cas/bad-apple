import os
import shutil
from yt_dlp import YoutubeDL
import ffmpeg
from PIL import Image
import multiprocessing
from playsound import playsound
import time
import json

OPTION_INVALID = "Invalid option. Try again."
CAN_CANCEL = "You can leave the field blank to keep the setting unchanged."
CANCEL = "Change operation canceled."
ERROR_FFMPEG = "[ERROR] ffmpeg has given an error, exiting"

COLOR_RESET = "\033[0m"
UNICODE_BLOCK = "\u2588"
CLEAR_COMMAND = "cls" if os.name == "nt" else "clear"

CONFIG_FILE = "config2.json"
VIDEO_FILE = "assets/video.webm"
AUDIO_FILE = "assets/audio.mp3"
ASCII_FILE = "assets/ascii.txt"
INFOS_FILE = "assets/info.json"

BAD_APPLE_URL = "https://www.youtube.com/watch?v=FtutLA63Cp8"

DEFAULT_CONFIG = {
    "default_path": BAD_APPLE_URL,
    "framerate": 30,
    "shade": True,
    "shading": [" ", ".", ":", "=", "#"],
    "color": False,
    "quiet": False,
    "delete_frames": False
}

def custom_output(stream, output_name):
    if config["quiet"]:
        return stream.output(output_name, loglevel="quiet")
    return stream.output(output_name)

def write_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def prompt(message: str, *options):
    print(message)
    
    for option in options: 
        print(f"  [{options.index(option) + 1}] {option}")

    user_input = input("Select an option: ")

    try:
        choice = int(user_input)
    except:
        for option in options:
            if user_input in option:
                choice = options.index(option) + 1
                break

    if not 0 < choice <= len(options):
        print(OPTION_INVALID)
        return prompt(message, *options)

    print()
    return choice

def ask_boolean(message: str):
    user_input = input(f"{message} [y/n, t/f]: ").lower()

    if user_input in ["true", "t", "yes", "y", "on", "1"]:
        return True
    elif user_input in ["false", "f", "no", "n", "off", "0"]:
        return False
    elif user_input == "":
        return "cancel"

    else:   
        print("You must answer true or false!")
        ask_boolean(message)

def whitespace():
    if not config["quiet"]:
        print()

def generate():
    print(f"Please enter a video URL or local path, or leave blank for fallback '{config['default_path']}'")
    path = input("Path/URL: ")

    if not path: 
        path = config["default_path"]

    if os.path.isdir("assets"):
        shutil.rmtree("assets")
    os.mkdir("assets")

    if "http://" in path or "https://" in path:
        print("[1/4] Downloading video...")
        
        opts = {"outtmpl": VIDEO_FILE}
        if config["quiet"]:
            opts["quiet"] = True

        try:
            YoutubeDL(opts).download(path)
        
        except:
            print("[ERROR] yt-dlp has given an error, exiting")
            return
    
    else:
        print("[1/4] Converting video...")

        if not os.path.isfile(path):
            print(f"[ERROR] There is no file at '{path}'")
            return

        try:
            stream = ffmpeg.input(path)
            stream = custom_output(stream, VIDEO_FILE)
            stream.run()
        
        except:
            print(ERROR_FFMPEG)
            return

    if not os.path.isfile(VIDEO_FILE):
        print(f"[ERROR] The video has seemed to have disappeared?!")
        return

    whitespace()

    print("[2/4] Extracting audio from video...")

    if os.path.isfile(AUDIO_FILE):
        os.path.remove(AUDIO_FILE)

    try:
        stream = ffmpeg.input(VIDEO_FILE)
        stream = custom_output(stream, AUDIO_FILE)
        stream.run()

    except:
        print(ERROR_FFMPEG)
        return

    whitespace()

    print("[3/4] Extracting frames from video (this may take longer)...")

    if os.path.isdir("frames"):
        shutil.rmtree("frames")
    os.mkdir("frames")

    try:
        stream = ffmpeg.input(VIDEO_FILE)
        stream = stream.filter("fps", fps=str(config["framerate"]))
        stream = custom_output(stream, "frames/frame_%06d.png")
        stream.run()

    except:
        print(ERROR_FFMPEG)
        return

    whitespace()

    terminal_size_obj = os.get_terminal_size()
    terminal_size = [terminal_size_obj.columns, terminal_size_obj.lines]

    print(f"[4/4] Generating ASCII art from frames... ({terminal_size[0]}x{terminal_size[1]})")

    text_frames = []
    frame_files = os.listdir("frames")
    frame_files.sort()
    count = 0

    for frame in frame_files:
        path = os.path.join("frames", frame)

        image = Image.open(path)
        image = image.resize((terminal_size[0], terminal_size[1] - 1))
        image = image.convert("RGB")
        
        text_frame = ""

        for pixel_rgb in list(image.getdata()):
            r = pixel_rgb[0]
            g = pixel_rgb[1]
            b = pixel_rgb[2]

            if config["shade"]:
                brightness = int((r + g + b) / 3)

                if   brightness <= 51:  pixel = config["shading"][0]
                elif brightness <= 102: pixel = config["shading"][1]
                elif brightness <= 153: pixel = config["shading"][2]
                elif brightness <= 204: pixel = config["shading"][3]
                elif brightness <= 255: pixel = config["shading"][4]
                else:                   pixel = "?"

            else:
                pixel = UNICODE_BLOCK

            if config["color"]: pixel = f"\033[38;2;{r};{g};{b}m{pixel}"

            text_frame += pixel

        text_frames.append(text_frame)
        count += 1

        if not config["quiet"] and (count % 100 == 0 or count == len(frame_files)):
            print(f"Processed {count} frames, {round(count / len(frame_files) * 100, 2)}% complete")

    if os.path.isfile(ASCII_FILE):
        os.remove(ASCII_FILE)

    with open(ASCII_FILE, "a") as f:
        for frame in text_frames:
            f.write(frame + "\n")

    if config["delete_frames"]:
        try:
            shutil.rmtree("frames")
        except:
            pass

    whitespace()

    if os.path.isfile(INFOS_FILE):
        os.remove(INFOS_FILE)

    infos = {
        "framerate": config["framerate"],
        "terminal_size": terminal_size,
        "color": config["color"]
    }

    infos["shading"] = config["shading"] if config["shade"] else UNICODE_BLOCK

    with open(INFOS_FILE, "w") as f:
        json.dump(infos, f, indent=4)

    print("Your video has been generated!")
    print("Exiting to menu, make sure to save your video with option 3 if you want to!")

def play():
    print("Please enter the name of a stored sequence or leave blank for the currently loaded one.")
    load = input("Name: ")

    if not load:
        directory = "assets"
    else:
        directory = os.path.join("stored", load)

    if not os.path.isdir(directory):
        print("Saved sequence not found, exiting")
        return

    ascii_file = os.path.join(directory, "ascii.txt")
    audio_file = os.path.join(directory, "audio.mp3")
    infos_file = os.path.join(directory, "info.json")

    if not os.path.isfile(ascii_file):
        print("You need at least a text file! exiting")
        return

    if os.path.isfile(audio_file):
        play_audio = True
    else:
        print("No audio file found, this will be bland methinks...")
        play_audio = False

    if os.path.isfile(infos_file):
        with open(infos_file, "r") as f:
            data = json.load(f)

        print(f"Found info: {data['framerate']} FPS, {data['terminal_size'][0]}x{data['terminal_size'][1]}, color: {data['color']}, shading: {data['shading']}")
        print("You will need to set your terminal size to the WxH value above for the playback to work properly.")

    else:
        print("No information file found, using default values")
        data = {
            "framerate": config["framerate"],
        }

    with open(ascii_file, "r") as f:
        text_frames = f.read().splitlines()

    if config["color"]: print("\033[0m")

    input("\n[READY] Playback is ready. Press enter to play." )

    os.system(CLEAR_COMMAND)

    if play_audio:
        audio_playback = multiprocessing.Process(target=playsound, args=(audio_file,), daemon=True)
        audio_playback.start()

    for frame in text_frames:
        print(frame)
        time.sleep(1 / data["framerate"])

    if play_audio and audio_playback.is_alive():
        audio_playback.terminate()

    if config["color"]: print("\033[0m")

    input("\nThanks for watching! Press enter to return to the main menu.")

def save():
    print("Sequence saver utility")

    if not os.path.isdir("stored"):
        os.mkdir("stored")

    if not os.path.isfile(ASCII_FILE):
        print("No ASCII file detected in main directory, cannot save this sequence")
        return

    print("Please enter a name to store this sequence, or leave blank to quit.")
    name = input("Name: ")

    if not name:
        print(CANCEL)
        return

    store_dir = os.path.join("stored", name)

    if os.path.isdir(store_dir):
        print(f"A sequence called '{name}' already exists")
        ch = ask_boolean("Overwrite?")

        if ch:
            shutil.rmtree(store_dir)

        else:
            print("Okay, but you'll need to pick a different name.\n")
            save()
            return

    os.mkdir(store_dir)

    shutil.copy(ASCII_FILE, store_dir)

    try:
        shutil.copy(AUDIO_FILE, store_dir)
    except:
        pass

    try:
        shutil.copy(INFOS_FILE, store_dir)
    except:
        pass

    print(f"Stored your sequence as '{name}'")

def edit_config(resume = None):
    if resume:
        ch = resume
    else:
        ch = prompt(
            "\nEditing config file.",
            f"Default video URL/path: {config['default_path']}",
            f"Framerate: {config['framerate']}",
            f"Shading on/off: {config['shade']}",
            f"Shading levels: {config['shading']}",
            f"Use ANSI colors: {config['color']}",
            f"Quiet output: {config['quiet']}",
            f"Delete frames after: {config['delete_frames']}",
            "Reset All Settings",
            "Back"
        )

    if ch == 1:
        print(f"The default video path or URL is '{config['default_path']}'. You can leave it blank to keep the current thing or type '!reset' to put the Bad Apple!! url back.")
        ch = input("New path or URL: ")
        
        if ch:
            if ch == "!reset":
                config["default_path"] = BAD_APPLE_URL

            else:
                config["default_path"] = ch
                write_config()
                print(f"Video path has been set to '{config['default_path']}'")

        else:
            print(CANCEL)

    elif ch == 2:
        print(f"The framerate is set to {config['framerate']} FPS.")
        ch = input("New framerate: ")

        if ch:
            try:
                config["framerate"] = int(ch)

            except:
                print("The framerate provided must be an integer!")
                edit_config(2)

            else:
                write_config()
                print(f"Framerate has been set to {config['framerate']}")

        else:
            print(CANCEL)

    elif ch == 3:
        print(f"Whether to use shading is set to {config['shade']}. If this is set to false, one character will be used for all shades (useful in conjunction with colors)")
        ch = ask_boolean("Use shading?")

        if ch == "cancel":
            print(CANCEL)

        else:
            config["shade"] = ch
            write_config()
            print(f"Whether to use shading has been set to {config['shade']}")

    elif ch == 4:
        print("Shading characters. Please enter one character per level, or leave blank to keep current character.")

        count = 0
        for level in range(5):
            range_text = f"{level * 20}-{level * 20 + 20}"
            while len(range_text) < 6:
                range_text = " " + range_text

            char = input(f"{range_text}% [now {config['shading'][level]}]: ")

            if not char:
                pass

            else:
                count += 1

                if len(char) > 1:
                    char_old = char
                    char = char[0]
                    print(f"'{char_old}' has been shortened to '{char}'")

                config["shading"][level] = char

        write_config()
        print(f"Changed {count} shading levels. They are now {config['shading']}")

    elif ch == 5:
        print(f"Whether to use colors is set to {config['color']}. This uses ANSI escape codes to make colors, and takes up ~18x more space.")
        ch = ask_boolean("Use color?")

        if ch == "cancel":
            print(CANCEL)

        else:
            config["color"] = ch
            write_config()
            print(f"Whether to use color codes has been set to {config['color']}")

    elif ch == 6:
        print(f"Quiet output is set to {config['quiet']}")
        ch = ask_boolean("Quiet?")

        if ch == "cancel":
            print(CANCEL)

        else:
            config["quiet"] = ch
            write_config()
            print(f"Quiet output has been set to {config['quiet']}")

    elif ch == 7:
        print(f"Delete image frames after rendering (to save space) is set to {config['delete_frames']}")
        ch = ask_boolean("Delete frames?")

        if ch == "cancel":
            print(CANCEL)
        
        else:
            config["delete_frames"] = ch
            write_config()
            print(f"Delete frames after has been set to {config['delete_frames']}")

    elif ch == 8:
        try:
            os.remove(CONFIG_FILE)
        except:
            pass

        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

        print("Settings have been reset")

    elif ch == 9:
        print("Exiting to main menu\n")
        return

    else:
        print(OPTION_INVALID)

    edit_config()

def main():
    ch = prompt(
        "\nWelcome to the Bad Apple!! renderer. Please select an option.",
        "Generate ASCII (will overwrite old sequence)",
        "Play/load generated ASCII",
        "Save generated ASCII",
        "Change settings",
        "Delete files",
        "Quit"
    )

    if ch == 1:
        generate()

    elif ch == 2:
        play()

    elif ch == 3:
        save()

    elif ch == 4:
        edit_config()

    elif ch == 5:
        for filename in ["video.webm", "audio.mp3", "ascii.txt", "info.json"]:
            try:
                os.remove(os.path.join("assets", filename))
            except:
                pass

        try:
            shutil.rmtree("frames")
        except:
            pass

    elif ch == 6:
        print("Goodbye!")
        return

    else:
        print(OPTION_INVALID)
        main()

    main()

if __name__ == "__main__":
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

        print("Generated config file!")

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    multiprocessing.set_start_method("fork")

    main()