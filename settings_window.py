from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QComboBox

class SettingsWindow(QWidget):
   def __init__(self):
      super().__init__()

      # UI Elements

      self.choice_prefereded_codec = QComboBox()
      self.choice_prefereded_codec.addItems(["mp3", "aac", "opus", "m4a", "wav", "flac"])

      # Layout
      layout = QVBoxLayout()

      layout.addWidget(self.choice_prefereded_codec)
      
      self.setLayout(layout)
