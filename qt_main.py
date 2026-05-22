import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from download_window import DownloadWindow
from settings_window import SettingsWindow
from config import Config

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
   
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())