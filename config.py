class Config:
   def __init__(self, path_config="config.json", yt_dlp_config="yt-dlp-config.json"):
      self.path_config = path_config
      self.yt_dlp_config = yt_dlp_config
      self.config = self.load_config()
      self.yt_dlp_config_data = self.load_yt_dlp_config()

   def load_config(self):
      import json
      with open(self.path_config, 'r') as f:
         return json.load(f)

   def load_yt_dlp_config(self):
      import json
      with open(self.yt_dlp_config, 'r') as f:
         return json.load(f)
   