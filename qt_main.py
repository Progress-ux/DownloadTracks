import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QProgressBar
from PySide6.QtCore import QThread, Signal
import os
from config import Config
from video_download import VideoDownloader
class DownloadThread(QThread):
   progress = Signal(int)
   finished = Signal(str)
   log_message = Signal(str)

   def __init__(self, urls, config):
      super().__init__()
      self.urls = urls
      self.config = config

   def run(self):
      video_downloader = VideoDownloader()

      for i, url in enumerate(self.urls, start=1):
         try:
            output_dir = self.config.config.get("output", "downloads")
            info = video_downloader.download_track(
               url.strip(), 
               self.config.yt_dlp_config_data, 
               i,
               outtmpl=os.path.join(output_dir, "temp.%(ext)s"),
               qt_signal=self.progress,
               qt_log_signal=self.log_message
            )

            video_downloader.save_track(
               info, 
               output_dir
            )

            filename = f"{video_downloader.get_safe_artist()} - {video_downloader.get_safe_title()}.mp3"
            track_path = os.path.join(output_dir, filename)

            video_downloader.add_tags(track_path)

            video_downloader.add_thumbnail(
               track_path,
               str(info.get("thumbnail", ""))
            )
            self.log_message.emit(f"✅ Загрузка {filename} завершена")


         except FileExistsError as e:
            self.log_message.emit(f"❌ Пропуск: {e}")
         
         except Exception as e:
            self.log_message.emit(f"❌ Ошибка при загрузке {url}: {e}")
            continue
      self.log_message.emit("Загрузка завершена")

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("YouTube MP3 Downloader")
      self.setGeometry(100, 100, 800, 600)

      # UI Elements
      self.url_input = QTextEdit()
      self.url_input.setPlaceholderText("Вставьте ссылки на YouTube (через пробел, запятую или построчно).")
      self.btn_download = QPushButton("Скачать все")
      self.progress_bar = QProgressBar()
      self.log_message = QTextEdit()
      self.log_message.setReadOnly(True)

      # Layout
      layout = QVBoxLayout()
      layout.addWidget(self.url_input)
      layout.addWidget(self.btn_download)
      layout.addWidget(self.progress_bar)
      layout.addWidget(self.log_message)
      container = QWidget()
      container.setLayout(layout)
      self.setCentralWidget(container)

      self.btn_download.clicked.connect(self.start_download)

      self.config = Config()
      self.create_output_folder(self.config.config.get("output", "downloads"))

   def create_output_folder(self, output_folder):
      if not os.path.exists(output_folder):
         os.makedirs(output_folder)

   def start_download(self):
      urls = self.url_input.toPlainText().strip()
      if not urls:
         return

      url_list = [url.strip() for url in urls.replace(",", " ").split() if url.strip()]
      self.download_thread = DownloadThread(url_list, self.config)
      self.download_thread.progress.connect(self.update_progress)
      self.download_thread.finished.connect(self.download_finished)
      self.download_thread.log_message.connect(self.log_message.append)
      self.download_thread.start()

   def update_progress(self, value):
      self.progress_bar.setValue(value)

   def download_finished(self, message):
      self.progress_bar.setValue(100)
      print(message)
   
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())