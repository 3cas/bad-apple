import json

with open("config.json", "r") as f:
    config = json.load(f)

config["youtube_url"] = "https://www.youtube.com/watch?v=FtutLA63Cp8"

with open("config.json", "w") as f:
    json.dump(config, f, indent=4)