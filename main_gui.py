#!/usr/bin/env python3

import sys
import logging
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

args = parser.parse_args()
log_mode = logging.DEBUG

if not args.debug:
    log_mode = logging.INFO

filename_log = Path.home() / ".local/state/DownloadTrack/download_gui.log"
filename_log.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=log_mode,
    filename=filename_log,
    encoding="utf-8",
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
