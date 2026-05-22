from PySide6.QtWidgets import QProgressBar, QTextEdit, QVBoxLayout, QPushButton, QWidget
from ui.worker import DownloadThread
from infrastructure.config_manager import Config
import os

class DownloadWindow(QWidget):
   def __init__(self, config):
      super().__init__()

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

      self.setLayout(layout)
      self.btn_download.clicked.connect(self.start_download)

      self.config = config
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
      self.log_message.ensureCursorVisible()

      self.download_thread.start()

   def update_progress(self, value):
      self.progress_bar.setValue(value)

   def download_finished(self):
      self.progress_bar.setValue(100)