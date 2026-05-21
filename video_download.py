from typing import Any
import os
import re
import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error # type: ignore
class VideoDownloader:
   def __init__(self):
      self._safe_artist = "Unknown"
      self._safe_title = "Unknown"
      self.qt_log_signal = None
      self.qt_signal = None
   
   def get_safe_artist(self) -> str: return self._safe_artist
   def get_safe_title(self) -> str: return self._safe_title

   def progress_hook(self, d):
      if d['status'] == 'downloading' and self.qt_signal is not None:
         downloaded = d.get('downloaded_bytes', 0)
         total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0

         if total > 0:
            percent = int((downloaded / total) * 100)
            self.qt_signal.emit(percent)
   
   def download_track(
      self,
      url: str, 
      yt_dlp_config: dict[str, Any], 
      number: int,
      outtmpl: str = "temp.%(ext)s",
      qt_signal=None,
      qt_log_signal=None
   ):
      if os.path.exists(outtmpl):
         os.remove(outtmpl)
         
      self.qt_signal = qt_signal
      self.qt_log_signal = qt_log_signal

      self.qt_log_signal.emit(f"+ \n{number}. Скачиваю: {url}") # type: ignore

      local_yt_dlp: dict[str, Any] = yt_dlp_config.copy()

      local_yt_dlp["outtmpl"] = outtmpl
      local_yt_dlp["progress_hooks"] = [self.progress_hook]

      with yt_dlp.YoutubeDL(local_yt_dlp) as ydl: # type: ignore
         info = ydl.extract_info(url, download=True)
      
      if not info:
         raise Exception("Не удалось получить информацию о треке")
      
      return info
   
   def save_track(self, info, output_folder: str):
      artist = info.get("uploader", "Unknown")
      title = info.get("title", "Unknown")

      self._safe_artist = re.sub(r'[<>:"/\\|?*]', "", str(artist))
      self._safe_title = re.sub(r'[<>:"/\\|?*]', "", str(title))

      filename = f"{self._safe_artist} - {self._safe_title}.mp3"

      temp_file_path = os.path.join(output_folder, "temp.mp3")
      final_file_path = os.path.join(output_folder, filename)

      try:
         if os.path.exists(final_file_path):
            if os.path.exists(temp_file_path):
               os.remove(temp_file_path)
            raise FileExistsError(f"Файл {filename} уже существует")

         if os.path.exists(temp_file_path):
            os.replace(temp_file_path, final_file_path)
            self.qt_log_signal.emit(f"+ Аудио сохранено как: {filename}") # type: ignore
         else: 
            raise FileNotFoundError(f"Временный файл {temp_file_path} не найден")
      except Exception as e:
         raise Exception("Не удалось сохранить трек")
      
   def add_tags(self, track_path: str):
      try:
         tags = EasyID3(track_path)
      except Exception as e:
         raise Exception(f"Ошибка при чтении ID3 тегов: {e}")

      tags["artist"] = self._safe_artist
      tags["title"] = self._safe_title
      tags.save(track_path)
      
   def add_thumbnail(self, track_path: str, thumbnail_url: str):
      try:
         tags = ID3(track_path)
      except error:
         raise Exception("Ошибка при чтении ID3 тегов. Убедитесь, что файл существует и является MP3.")
      
      try:
         import requests
         response = requests.get(thumbnail_url, timeout=5)
         response.raise_for_status()
         thumbnail_data = response.content
      except Exception as e:
         raise Exception(f"Ошибка при загрузке обложки: {e}")

      try:
         tags.add(APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=thumbnail_data
         ))

         tags.save(track_path)
      except Exception as e:
         raise Exception(f"Не удалось добавить обложку в ID3 теги: {e}")