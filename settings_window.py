from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QComboBox

class SettingsWindow(QWidget):
   def __init__(self):
      super().__init__()

      # UI Elements
      self.choice_prefereded_codec = QComboBox()
      self.choice_prefereded_codec.addItems(["mp3", "aac", "opus", "m4a", "wav", "flac"])

      self.choice_prefereded_quality = QComboBox()
      self.choice_prefereded_quality.addItems(["128", "192", "256", "320", "0"])

      # Layout
      layout = QVBoxLayout()

      layout.addWidget(self.choice_prefereded_codec)
      layout.addWidget(self.choice_prefereded_quality)

      self.setLayout(layout)
