import os
import shutil
from yt_dlp import YoutubeDL
import ffmpeg
from PIL import Image
import multiprocessing
from playsound import playsound
import time

# Options that you can change!
VIDEO_NAME = "video.webm"
YOUTUBE_URL = ["https://www.youtube.com/watch?v=FtutLA63Cp8"]
FRAMERATE = 30
QUIET = True
SKIP_SETUP = False
CHAR_LIGHT = "#"
CHAR_DARK = " "

VIDEO_FILE = f"assets/{VIDEO_NAME}"
AUDIO_FILE = os.path.join("assets", "audio.mp3")
ASCII_FILE = os.path.join("assets", "ascii.txt")

clear_command = "cls" if os.name == "nt" else "clear"

def custom_output(stream, output_name):
    if QUIET:
        return stream.output(output_name, loglevel="quiet")
    return stream.output(output_name)

if not(os.path.isfile(ASCII_FILE) and os.path.isfile(AUDIO_FILE) and SKIP_SETUP):
    if SKIP_SETUP:
        print("Audio and ASCII art are required to skip setup, running setup")
        if not QUIET:
            print()

    if not os.path.isfile(os.path.join("assets", VIDEO_NAME)):
        print("[1/4] Downloading Bad Apple!! video...")

        opts = {"outtmpl": VIDEO_FILE}
        if QUIET:
            opts["quiet"] = True

        YoutubeDL(opts).download(YOUTUBE_URL)
    else:
        print("[1/4] Video found, continuing!")

    if not QUIET:
        print()

    print("[2/4] Extracting audio from video...")
    if os.path.isfile(AUDIO_FILE):
        os.remove(AUDIO_FILE)

    stream = ffmpeg.input(VIDEO_FILE)
    stream = custom_output(stream, "assets/audio.mp3")
    stream.run()

    if not QUIET:
        print()

    print("[3/4] Extracting frames from video...")
    if os.path.isdir("frames"):
        shutil.rmtree("frames")
    os.mkdir("frames")
    
    stream = ffmpeg.input(VIDEO_FILE)
    stream = stream.filter("fps", fps=str(FRAMERATE))
    stream = custom_output(stream, "frames/frame_%06d.png")
    stream.run()

    if not QUIET:
        print()

    print("[4/4] Generating ASCII art from frames...")
    terminal_size = os.get_terminal_size()
    text_frames = []
    frame_files = os.listdir("frames")
    frame_files.sort()
    count = 0

    for frame in frame_files:
        path = os.path.join("frames", frame)

        image = Image.open(path)
        image = image.resize((terminal_size.columns, terminal_size.lines - 1))
        
        text_frame = ""
        for pixel_brightness in image.getdata(0):
            if pixel_brightness > 50:
                text_frame += CHAR_LIGHT
            else:
                text_frame += CHAR_DARK

        text_frames.append(text_frame)
        count += 1

        if not QUIET and (count % 100 == 0 or count == len(frame_files)):
            print(f"Processed {count} frames, {round(count / len(frame_files) * 100, 2)}% complete")

    if os.path.isfile(ASCII_FILE):
        os.remove(ASCII_FILE)

    with open(ASCII_FILE, "a") as f:
        for frame in text_frames:
            f.write(frame + "\n")

else:
    with open(ASCII_FILE, "r") as f:
        text_frames = f.read().splitlines()

    print("Skipped setup, using cached audio and ASCII!")

input("\n[READY] Bad Apple!! is ready. Press enter to play." )

os.system(clear_command)

multiprocessing.set_start_method("fork")
play_audio = multiprocessing.Process(target=playsound, args=(AUDIO_FILE,), daemon=True)
play_audio.start()

for frame in text_frames:
    print(frame)
    time.sleep(1 / FRAMERATE)

if play_audio.is_alive():
    play_audio.terminate()