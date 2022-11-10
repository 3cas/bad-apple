import os
import shutil

for filename in ["video.webm", "audio.mp3", "ascii.txt"]:
    try:
        os.remove(os.path.join("assets", filename))
    except:
        pass

try:
    shutil.rmtree("frames")
except:
    pass