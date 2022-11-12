import os
import shutil
from yt_dlp import YoutubeDL
import ffmpeg
from PIL import Image
import multiprocessing
from playsound import playsound
import time
import json

from reset import reset_files

if not os.path.isfile("config.json"):
    default_options = {
        "youtube_url": "https://www.youtube.com/watch?v=FtutLA63Cp8",
        "video_name": "video.webm",
        "framerate": 30,
        "quiet": False,
        "skip_setup": False,
        "auto_reset": False,
        "shading": [" ", ".", "/", "X", "#"]
    }

    with open("config.json", "w") as f:
        json.dump(default_options, f, indent=4)

    print("Generated config file!")

with open("config.json", "r") as f:
    config = json.load(f)

if config["auto_reset"]:
    reset_files()

video_file = f"assets/{config['video_name']}"
audio_file = os.path.join("assets", "audio.mp3")
ascii_file = os.path.join("assets", "ascii.txt")

clear_command = "cls" if os.name == "nt" else "clear"

def custom_output(stream, output_name):
    if config["quiet"]:
        return stream.output(output_name, loglevel="quiet")
    return stream.output(output_name)

if not(os.path.isfile(ascii_file) and os.path.isfile(audio_file) and config["skip_setup"]):
    if config["skip_setup"]:
        print("Audio and ASCII art are required to skip setup, running setup")
        if not config["quiet"]:
            print()

    if not os.path.isfile(os.path.join("assets", config["video_name"])):
        print("[1/4] Downloading Bad Apple!! video...")

        opts = {"outtmpl": video_file}
        if config["quiet"]:
            opts["quiet"] = True

        YoutubeDL(opts).download(config["youtube_url"])
    else:
        print("[1/4] Video found, continuing!")

    if not config["quiet"]:
        print()

    print("[2/4] Extracting audio from video...")
    if os.path.isfile(audio_file):
        os.remove(audio_file)

    stream = ffmpeg.input(video_file)
    stream = custom_output(stream, "assets/audio.mp3")
    stream.run()

    if not config["quiet"]:
        print()

    print("[3/4] Extracting frames from video...")
    if os.path.isdir("frames"):
        shutil.rmtree("frames")
    os.mkdir("frames")
    
    stream = ffmpeg.input(video_file)
    stream = stream.filter("fps", fps=str(config["framerate"]))
    stream = custom_output(stream, "frames/frame_%06d.png")
    stream.run()

    if not config["quiet"]:
        print()

    terminal_size = os.get_terminal_size()
    print(f"[4/4] Generating ASCII art from frames... ({terminal_size.columns}x{terminal_size.lines})")
    text_frames = []
    frame_files = os.listdir("frames")
    frame_files.sort()
    count = 0

    for frame in frame_files:
        path = os.path.join("frames", frame)

        image = Image.open(path)
        image = image.resize((terminal_size.columns, terminal_size.lines - 1))
        image = image.convert("RGB")
        
        text_frame = ""

        for pixel_rgb in list(image.getdata()):
            brightness = int((pixel_rgb[0] + pixel_rgb[1] + pixel_rgb[2]) / 3)

            if brightness <= 51:
                text_frame += config["shading"][0]
            elif brightness <= 102:
                text_frame += config["shading"][1]
            elif brightness <= 153:
                text_frame += config["shading"][2]
            elif brightness <= 204:
                text_frame += config["shading"][3]
            elif brightness <= 255:
                text_frame += config["shading"][4]
            else:
                print("huh")

        text_frames.append(text_frame)
        count += 1

        if not config["quiet"] and (count % 100 == 0 or count == len(frame_files)):
            print(f"Processed {count} frames, {round(count / len(frame_files) * 100, 2)}% complete")

    if os.path.isfile(ascii_file):
        os.remove(ascii_file)

    with open(ascii_file, "a") as f:
        for frame in text_frames:
            f.write(frame + "\n")

    if config["delete_frames"]:
        try:
            shutil.rmtree("frames")
        except:
            pass

else:
    with open(ascii_file, "r") as f:
        text_frames = f.read().splitlines()

    print("Skipped setup, using cached audio and ASCII!")

input("\n[READY] Bad Apple!! is ready. Press enter to play." )

os.system(clear_command)

multiprocessing.set_start_method("fork")
play_audio = multiprocessing.Process(target=playsound, args=(audio_file,), daemon=True)
play_audio.start()

for frame in text_frames:
    print(frame)
    time.sleep(1 / config["framerate"])

if play_audio.is_alive():
    play_audio.terminate()