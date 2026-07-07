import json
from pathlib import Path


class Config:
    def __init__(self, path_config: Path = Path("config.json")):
        self.path_config: Path = path_config
        self.config = self.load_config()

    def _create_default_config(self):
        default_config = {
            "output": "~/Downloads/",
            "yt-dlp-config": {
                "format": "bestaudio/best",
                "noplaylist": True,
                "outtmpl": "%(title)s.%(ext)s",
                "quiet": True,
                "noprogress": True,
                "extractor_args": {"youtube": {"player_client": ["web", "android"]}},
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            },
        }

        self.path_config.parent.mkdir(parents=True, exist_ok=True)

        with open(self.path_config, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

    def load_config(self):
        if not self.path_config.exists():
            self._create_default_config()

        with open(self.path_config, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_config(self):
        with open(self.path_config, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=3, ensure_ascii=False)

    @property
    def yt_dlp_data(self):
        return self.config.get("yt-dlp-config", {})
