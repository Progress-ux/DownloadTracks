from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QComboBox, QLineEdit, QPushButton

class SettingsWindow(QWidget):
   def __init__(self):
      super().__init__()

      # UI Elements
      self.choice_preferred_codec = QComboBox()
      self.choice_preferred_codec.addItems(["mp3", "aac", "opus", "m4a", "wav", "flac"])

      self.choice_preferred_quality = QComboBox()
      self.choice_preferred_quality.addItems(["128", "192", "256", "320", "0"])

      self.save_path = QLineEdit()
      self.save_path.setPlaceholderText("Путь для сохранения треков (по умолчанию: папка 'downloads' в текущей директории)")

      self.btn_output_folder = QPushButton("Выбрать папку для сохранения")

      # Layout
      layout = QVBoxLayout()

      layout.addWidget(self.choice_preferred_codec)
      layout.addWidget(self.choice_preferred_quality)
      layout.addWidget(self.save_path)
      layout.addWidget(self.btn_output_folder)

      self.setLayout(layout)
