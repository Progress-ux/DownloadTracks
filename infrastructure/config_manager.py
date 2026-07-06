import json
from pathlib import Path

class Config:
    def __init__(self, folder_name="DownloadTracks", path_config="config.json"):
        self.config_dir = Path.home() / ".config" / folder_name
        self.path_config = self.config_dir / path_config

        self.config = self.load_config()

    def create_config(self):
        default_config = {
           "output": "~/Downloads/",
           "yt-dlp-config": {
              "format": "bestaudio/best",
              "noplaylist": True,
              "outtmpl": "%(title)s.%(ext)s",
              "quiet": True,
              "noprogress": True,
              "extractor_args": {
                 "youtube": {
                    "player_client": [
                       "web",
                       "android"
                    ]
                 }
              },
              "postprocessors": [
                 {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                 }
              ]
           }
        }
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.path_config, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

        return default_config

    def load_config(self):
        if not self.path_config.exists():
            return self.create_config()
        try:
            with open(self.path_config, 'r', encoding='utf-8') as f:
               return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self.create_config()
   
    def save_config(self):
       with open(self.path_config, 'w', encoding='utf-8') as f:
          json.dump(self.config, f, indent=4, ensure_ascii=False)
   
    @property
    def yt_dlp_data(self):
       return self.config.get("yt-dlp-config", {})
