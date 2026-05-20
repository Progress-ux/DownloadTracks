from tqdm import tqdm
from typing import Any
import os
import re


class VideoDownloader:
   def __init__(self):
      self.pbar = None
      self._safe_artist = "Unknown"
      self._safe_title = "Unknown"
   
   def get_safe_artist(self) -> str: return self._safe_artist
   def get_safe_title(self) -> str: return self._safe_title

   def progress_hook(self, d):
      if d['status'] == 'downloading':
         if self.pbar is None:
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            self.pbar = tqdm(total=total, unit='B', unit_scale=True, desc='Downloading')
         self.pbar.update(d['downloaded_bytes'] - self.pbar.n)
      elif d['status'] == 'finished':
         if self.pbar:
            self.pbar.close()
            self.pbar = None
            print("✅ Загрузка завершена")
   
   def download_track(
      self,
      url: str, 
      yt_dlp_config: dict[str, Any], 
      number: int,
      outtmpl: str = "temp.%(ext)s",
   ):
      try:
         import yt_dlp
      except ImportError:
         raise Exception("Модуль yt_dlp не найден. Установка: pip install yt-dlp")
      
      print(f"\n{number}. Скачиваю: {url}")

      local_yt_dlp: dict[str, Any] = yt_dlp_config.copy()

      local_yt_dlp["outtmpl"] = outtmpl
      local_yt_dlp["progress_hooks"] = [self.progress_hook]

      with yt_dlp.YoutubeDL(local_yt_dlp) as ydl: # type: ignore
         info = ydl.extract_info(url, download=True)
      
      if not info:
         print(f"❌ Не удалось получить информацию о треке: {url}")
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
            print(f"Трек сохранен как: {filename}")
         else: 
            raise FileNotFoundError(f"Временный файл {temp_file_path} не найден")
      except Exception as e:
         print(f"Ошибка при переименовании файла: {e}")
         raise Exception("Не удалось сохранить трек")
      
   def add_tags(self, track_path: str):
      try:
         from mutagen.easyid3 import EasyID3
      except ImportError:
         raise Exception("Модуль mutagen не найден. Установка: pip install mutagen")

      try:
         tags = EasyID3(track_path)
      except Exception as e:
         raise Exception(f"Ошибка при чтении ID3 тегов: {e}")

      tags["artist"] = self._safe_artist
      tags["title"] = self._safe_title
      tags.save(track_path)
      
   def add_thumbnail(self, track_path: str, thumbnail_url: str):
      try:
         from mutagen.id3 import ID3, APIC, error # type: ignore
      except ImportError:
         raise Exception("Модуль mutagen не найден. Установка: pip install mutagen")

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