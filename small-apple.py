import os,PIL.Image as i,playsound as s,threading as t,time
d,p=os.get_terminal_size(),";ffmpeg -i v.webm "
os.system(f"yt-dlp -o v youtu.be/FtutLA63Cp8{p}a.mp3{p}-filter:v fps=30 %4d.png")
o=["".join(["# "[p>9]for p in i.open(f).resize((d.columns,d.lines-1)).convert("RGB").getdata(0)])for f in sorted(os.listdir())[:-2]]
t.Thread(target=s.playsound,args=["a.mp3"],daemon=True).start()
for p in o:print(p);time.sleep(1/30)