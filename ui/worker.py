import os
from core.downloader import VideoDownloader
from core.video_processor import VideoProcessor
from core.yt_dlp_logger import NoWarningLogger
from PySide6.QtCore import QThread, Signal

class DownloadThread(QThread):
   progress = Signal(int)
   finished = Signal(str)
   log_message = Signal(str)

   def __init__(self, urls, config):
      super().__init__()
      self.urls = urls
      self.config = config
      self.config.config["yt-dlp-config"]["logger"] = NoWarningLogger(self.log_message.emit)

   def run(self):
      video_downloader = VideoDownloader(self.progress.emit, self.log_message.emit)
      video_processor = VideoProcessor(
         log_callback=self.log_message.emit
      )

      for i, url in enumerate(self.urls, start=1):
         try:
            output_dir = self.config.config.get("output", "downloads")

            # Downloads the track to temp.{ext}
            info = video_downloader.download_track(
               url.strip(), 
               self.config.config.get("yt-dlp-config", {}), 
               i,
               outtmpl=os.path.join(output_dir, "temp.%(ext)s"),
            )

            # Renames and saves a track
            filepath = video_processor.save_track(
               info, 
               output_dir
            )

            filename = f"{video_processor.get_safe_artist()} - {video_processor.get_safe_title()}{video_processor.get_extension()}"

            # Fills in tags
            video_processor.add_tags(filepath)

            # Writes to the thumbnail track
            video_processor.add_thumbnail(
               filepath,
               str(info.get("thumbnail", ""))
            )
            self.log_message.emit(f"+ Загрузка {filename} завершена")


         except FileExistsError as e:
            self.log_message.emit(f"- Пропуск: {e}")
            continue
         
         except Exception as e:
            self.log_message.emit(f"- Ошибка при загрузке {url}: {e}")
            continue
      self.log_message.emit("+ Загрузка завершена")