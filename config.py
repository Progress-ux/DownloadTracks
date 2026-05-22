import json


class Config:
   def __init__(self, path_config="config.json"):
      self.path_config = path_config
      self.config = self.load_config()

   def load_config(self):
      with open(self.path_config, 'r') as f:
         return json.load(f)
   
   def save_config(self):
      with open(self.path_config, 'w', encoding='utf-8') as f:
         json.dump(self.config, f, indent=3, ensure_ascii=False)
   
   @property
   def yt_dlp_data(self):
      return self.config.get("yt-dlp-config", {})