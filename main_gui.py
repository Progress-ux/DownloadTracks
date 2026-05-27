import sys
import logging
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

args = parser.parse_args()
log_mode = logging.DEBUG

if not args.debug:
   log_mode = logging.INFO

logging.basicConfig(
   level=log_mode, 
   filename="py_log.log", 
   encoding="utf-8",
   format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())