import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QProgressBar
import os
from config import Config
from download_thread import DownloadThread

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

   def download_finished(self):
      self.progress_bar.setValue(100)
   
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())