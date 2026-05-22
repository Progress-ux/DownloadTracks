from PySide6.QtWidgets import QMainWindow, QTabWidget
from ui.download_page import DownloadWindow
from ui.settings_page import SettingsWindow
from infrastructure.config_manager import Config

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("YouTube MP3 Downloader")
      self.setGeometry(100, 100, 800, 600)

      self.config = Config()
      
      self.download_window = DownloadWindow(config=self.config)
      self.settings_window = SettingsWindow(config=self.config)

      self.tabs = QTabWidget()

      self.tabs.addTab(self.download_window, "Скачивание")
      self.tabs.addTab(self.settings_window, "Настройки")

      self.setCentralWidget(self.tabs)
