import os
from PIL import Image
import multiprocessing
from playsound import playsound
import time
def s(t):os.system(t)
s("yt-dlp -o v youtu.be/FtutLA63Cp8")
s("ffmpeg -i v.webm a.mp3")
os.mkdir("f")
s("ffmpeg -i v.webm -filter:v fps=30 f/f%06d.png")
b=os.get_terminal_size()
c=[]
d=os.listdir("f")
d.sort()
e=0
for f in d:
    g=""
    for h in list(Image.open("f/"+f).resize((b.columns,b.lines-1)).convert("RGB").getdata()):
        i = int((h[0]+h[1]+h[2])/3)
        for j in [[51," "],[102,"."],[153,":"],[204,"="],[255,"#"]]:
            if i<=j[0]:
                g+=j[1]
                break
        c.append(g)
        e+=1
s("clear")
multiprocessing.set_start_method("fork")
k=multiprocessing.Process(target=playsound, args=("a.mp3",), daemon=True)
k.start()
for l in c:
    print(l)
    time.sleep(1/30)
if k.is_alive():
    k.terminate()