# bad-apple
Play any video (originally Bad Apple!!) in the terminal using Python

This project is heavily inspired by [Ubuntufanboy's Bad Apple!! code](https://github.com/Ubuntufanboy/bad-apple) and it uses the same method (but I wrote all the code myself).

Currently only runs properly on Linux. Mac is lacking audio, and I haven't tested Windows yet.

## How to Use

The CLI is a bit counter-intuitive at the moment, but I am working on improvements.

Basic Bad Apple!! usage:
1. `python -m pip install -r requirements.txt`
2. `python bad-apple.py`

### Configuration

The `config.json` file is generated upon running the script for the first time.

Config options:
- **youtube_url** - The URL for yt-dlp to download from
- **video_name** - The name to save the video file to, or to use if it is already in place
- **framerate** - The framerate of the output video
- **quiet** - The yt-dlp, ffmpeg, and ASCII conversion processes hide detail
- **skip_setup** - Skip audio and ASCII extraction if the files are in place
- **auto_reset** - Run `reset.py` to delete saved files and do a clean run every time
- **delete_frames** - Delete frames directory after generating ASCII, to save space
- **shading** - List of 5 shading gradients from light to dark

### Scripts

- `bad-apple.py` - Downloads and generates a Bad Apple!! video. It will generate the `config.json` file as well. You can press ctrl + C at any time to cancel any part of the script.
- `reset.py` - Deletes the saved video, audio, ASCII, and frames.
- `reset-url.py` - Automatically resets the URL to Bad Apple!! in `config.json`
- `store.py [name]` - Copies audio and ASCII to named storage directory. The argument is optional, it will ask you for the name.
- `load.py [name]` - Copies audio and ASCII from named storage into the main directories. It will overwrite whatever current files are downloaded.

### Bonus

`small-apple.py` is the result of me challenging myself to make a Bad Apple!! script as small as possible. It only plays Bad Apple!! and expects you to run it in a directory without files already in it. It is very counter-intuitive because I prioritized making it short. Only 452 characters! Also, as far as I know, Small Apple!! only runs properly on Linux, but feel free to try it on other operating systems.