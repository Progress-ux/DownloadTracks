from typing import Any
import os
import re
import requests
import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error # type: ignore

class VideoDownloader:
   def __init__(self, progress_callback=None, log_callback=None):

      self._safe_artist = "Unknown"
      self._safe_title = "Unknown"
      self._extension = ".mp3"
      self.progress_callback = progress_callback
      self.log_callback = log_callback
   
   def get_safe_artist(self) -> str: return self._safe_artist
   def get_safe_title(self) -> str: return self._safe_title
   def get_extension(self) -> str: return self._extension

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

      local_yt_dlp["outtmpl"] = outtmpl
      local_yt_dlp["progress_hooks"] = [self.progress_hook]

      with yt_dlp.YoutubeDL(local_yt_dlp) as ydl: # type: ignore
         info = ydl.extract_info(url, download=True)
      
      if not info:
         raise Exception("Не удалось получить информацию о треке")
      
      return info
   
   def save_track(self, info, output_folder: str):

      self.log_callback("Начинаю извлечение аудио") # type: ignore

      artist = info.get("uploader", "Unknown")
      title = info.get("title", "Unknown")

      if 'requested_downloads' in info and info['requested_downloads']:
        actual_temp_path = info['requested_downloads'][0].get('filepath')
      else:
         # Фолбэк, если по какой-то причине списка нет (хотя он должен быть)
         actual_temp_path = info.get('_filename')

      if not actual_temp_path or not os.path.exists(actual_temp_path):
         raise FileNotFoundError(f"Скачанный файл не найден по пути: {actual_temp_path}")

      extension = os.path.splitext(actual_temp_path)[1]
      self._extension = extension

      self._safe_artist = re.sub(r'[<>:"/\\|?*]', "", str(artist))
      self._safe_title = re.sub(r'[<>:"/\\|?*]', "", str(title))

      filename = f"{self._safe_artist} - {self._safe_title}{extension}"

      final_file_path = os.path.join(output_folder, filename)

      if os.path.exists(final_file_path):
         if os.path.exists(actual_temp_path):
            os.remove(actual_temp_path)
         raise FileExistsError(f"Файл {filename} уже существует")

      try:
         if os.path.exists(actual_temp_path):
            os.replace(actual_temp_path, final_file_path)
            self.log_callback(f"+ Аудио сохранено как: {filename}") # type: ignore
         else: 
            raise FileNotFoundError(f"Временный файл {actual_temp_path} не найден")
      except FileNotFoundError as e:
         raise Exception(e)
      except Exception as e:
         raise Exception(f"Критическая ошибка при сохранении трека: {e}")
      
   def add_tags(self, track_path: str):

      self.log_callback("Начинаю добавление тегов") # type: ignore

      try:
         tags = EasyID3(track_path)
      except Exception as e:
         raise Exception(f"Ошибка при чтении ID3 тегов: {e}")

      tags["artist"] = self._safe_artist
      tags["title"] = self._safe_title
      tags.save(track_path)
      self.log_callback("Теги успешно добавлены") # type: ignore
      
   def add_thumbnail(self, track_path: str, thumbnail_url: str):
      self.log_callback("Начинаю добавление обложки") # type: ignore

      try:
         tags = ID3(track_path)
      except error:
         raise Exception("Ошибка при чтении ID3 тегов. Убедитесь, что файл существует и является MP3.")
      
      try:
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
         self.log_callback("Обложка успешно добавлена") # type: ignore

      except Exception as e:
         raise Exception(f"Не удалось добавить обложку в ID3 теги: {e}")