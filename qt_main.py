import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QTextEdit
from download_window import DownloadWindow

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("YouTube MP3 Downloader")
      self.setGeometry(100, 100, 800, 600)
      
      download_window = DownloadWindow()
      self.tabs = QTabWidget()

      self.tabs.addTab(download_window.container, "Скачивание")
      self.tabs.addTab(QTextEdit("Настройки в разработке..."), "Настройки")

      self.setCentralWidget(self.tabs)
   
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())