import os
from core.downloader import VideoDownloader
from PySide6.QtCore import QThread, Signal

class DownloadThread(QThread):
   progress = Signal(int)
   finished = Signal(str)
   log_message = Signal(str)

   def __init__(self, urls, config):
      super().__init__()
      self.urls = urls
      self.config = config

   def run(self):
      video_downloader = VideoDownloader(self.progress.emit, self.log_message.emit)

      for i, url in enumerate(self.urls, start=1):
         try:
            output_dir = self.config.config.get("output", "downloads")

            # Downloads the track to temp.mp3
            info = video_downloader.download_track(
               url.strip(), 
               self.config.config.get("yt-dlp-config", {}), 
               i,
               outtmpl=os.path.join(output_dir, "temp.%(ext)s"),
            )

            # Renames and saves a track
            video_downloader.save_track(
               info, 
               output_dir
            )

            filename = f"{video_downloader.get_safe_artist()} - {video_downloader.get_safe_title()}.mp3"
            track_path = os.path.join(output_dir, filename)

            # Fills in tags
            video_downloader.add_tags(track_path)

            # Writes to the thumbnail track
            video_downloader.add_thumbnail(
               track_path,
               str(info.get("thumbnail", ""))
            )
            self.log_message.emit(f"+ Загрузка {filename} завершена")


         except FileExistsError as e:
            self.log_message.emit(f"- Пропуск: {e}")
         
         except Exception as e:
            self.log_message.emit(f"- Ошибка при загрузке {url}: {e}")
            continue
      self.log_message.emit("+ Загрузка завершена")