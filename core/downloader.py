from typing import Any
import yt_dlp
import os
import logging

class VideoDownloader:
   def __init__(self, progress_callback=None, log_callback=None):
      logging.debug("Init VideoDownloader")

      self.progress_callback = progress_callback
      self.log_callback = log_callback
   
   def progress_hook(self, d):
      if d['status'] == 'downloading' and self.progress_callback :
         downloaded = d.get('downloaded_bytes', 0)
         total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0

         if total > 0:
            percent = int((downloaded / total) * 100)
            self.progress_callback(percent)
   
   def download_track(
      self,
      url: str, 
      yt_dlp_config: dict[str, Any], 
      number: int,
      outtmpl: str = "temp.%(ext)s",
   ):

      if os.path.exists(outtmpl):
         os.remove(outtmpl)

      self.log_callback(f"\n+ {number}. Скачиваю: {url}") # type: ignore

      local_yt_dlp: dict[str, Any] = yt_dlp_config.copy()
      logging.debug(f"Используемый конфиг yt_dlp: {local_yt_dlp}")

      local_yt_dlp["outtmpl"] = outtmpl
      local_yt_dlp["progress_hooks"] = [self.progress_hook]

      with yt_dlp.YoutubeDL(local_yt_dlp) as ydl: # type: ignore
         info = ydl.extract_info(url, download=True)
      
      if not info:
         logging.error("Не удалось получить информацию о треке")
         raise Exception("Не удалось получить информацию о треке")
      
      return info