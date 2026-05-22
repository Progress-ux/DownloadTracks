from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QLineEdit, QPushButton, QLabel, QFormLayout, QGroupBox)
from PySide6.QtCore import Qt
from config import Config

class SettingsWindow(QWidget):
   def __init__(self, config: Config):
      super().__init__()
      self.config = config


      main_layout = QVBoxLayout()
      main_layout.setContentsMargins(20, 20, 20, 20)
      main_layout.setSpacing(15)

      # UI Elements

      # Settings audio
      audio_group = QGroupBox("Настройки качества")
      audio_layout = QFormLayout()
      audio_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
      audio_layout.setSpacing(10)

      self.choice_preferred_codec = QComboBox()
      self.choice_preferred_codec.addItems(["mp3", "aac", "opus", "m4a", "wav", "flac"])
      self.choice_preferred_codec.setFixedWidth(120)

      self.choice_preferred_quality = QComboBox()
      self.choice_preferred_quality.addItems(["128", "192", "256", "320", "0"])
      self.choice_preferred_quality.setFixedWidth(120)

      audio_layout.addRow("Формат аудио:", self.choice_preferred_codec)
      audio_layout.addRow("Качество (kbps):", self.choice_preferred_quality)
      audio_group.setLayout(audio_layout)

      # Settings save path
      path_group = QGroupBox("Сохранение")
      path_layout = QVBoxLayout()

      path_label = QLabel("Папка для загрузок:")
      path_input_layout = QHBoxLayout()
      self.save_path = QLineEdit()
      self.save_path.setPlaceholderText("По умолчанию ./downloads")
      self.save_path.setReadOnly(True)

      self.btn_output_folder = QPushButton("Обзор...")
      self.btn_output_folder.setFixedWidth(80)

      path_input_layout.addWidget(self.save_path)
      path_input_layout.addWidget(self.btn_output_folder)

      path_layout.addWidget(path_label)
      path_layout.addLayout(path_input_layout)
      path_group.setLayout(path_layout)

      # Loading settings from the config
      self.load_settings_to_ui()

      # Save button
      self.btn_save_settings = QPushButton("Сохранить")
      self.btn_save_settings.setFixedWidth(160)
      self.btn_save_settings.clicked.connect(self.save_settings)

      main_layout.addWidget(audio_group)
      main_layout.addWidget(path_group)
      main_layout.addWidget(self.btn_save_settings)
      main_layout.addStretch()

      self.setLayout(main_layout)

   def save_settings(self):
      new_codec = self.choice_preferred_codec.currentText()
      new_quality = self.choice_preferred_quality.currentText()
      new_path = self.save_path.text()

      if new_path:
         self.config.config["output"] = new_path
      
      pps = self.config.config["yt-dlp-config"].get("postprocessors", [])
      for pp in pps:
         if pp.get("key") == "FFmpegExtractAudio":
            pp["preferredcodec"] = new_codec
            pp["preferredquality"] = new_quality

      self.config.save_config()
     
   def load_settings_to_ui(self):
      current_path = self.config.config.get("output", "downloads")
      self.save_path.setText(current_path)

      yt_data = self.config.config.get("yt-dlp-config", {})
      pps = yt_data.get("postprocessors", [])

      # Default
      codec = "mp3"
      quality = "192"

      for pp in pps:
         if pp.get("key") == "FFmpegExtractAudio":
            codec = pp.get("preferredcodec", "mp3")
            quality = pp.get("preferredquality", "192")
            
      self.choice_preferred_codec.setCurrentText(codec)
      self.choice_preferred_quality.setCurrentText(quality)