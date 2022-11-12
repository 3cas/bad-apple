import os
import shutil

def reset_files():
    for filename in ["video.webm", "audio.mp3", "ascii.txt"]:
        try:
            os.remove(os.path.join("assets", filename))
        except:
            pass

    try:
        shutil.rmtree("frames")
    except:
        pass

if __name__ == "__main__":
    reset_files()