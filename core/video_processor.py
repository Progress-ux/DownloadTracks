from pathlib import Path
import re
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error  # type: ignore
import logging


class VideoProcessor:

    def __init__(self, log_callback=None):
        self.log_callback = log_callback

        self._safe_artist = "Unknown"
        self._safe_title = "Unknown"
        self._extension = ".mp3"

    def get_safe_artist(self) -> str:
        return self._safe_artist

    def get_safe_title(self) -> str:
        return self._safe_title

    def get_extension(self) -> str:
        return self._extension

    def _get_filepath(self, info) -> Path:
        actual_temp_path = ""

        if "requested_downloads" in info and info["requested_downloads"]:
            actual_temp_path_str = info["requested_downloads"][0].get("filepath")
        else:
            logging.warning("В requested_downloads не найден filepath")
            actual_temp_path_str = info.get("_filename")

        actual_temp_path = Path(actual_temp_path_str) if actual_temp_path_str else None
        if not actual_temp_path or not actual_temp_path.exists():
            logging.error(f"Скачанный файл не найден по пути: {actual_temp_path}")
            raise FileNotFoundError(
                f"Скачанный файл не найден по пути: {actual_temp_path}"
            )

        return actual_temp_path

    def save_track(self, info, output_folder: Path) -> Path:

        self.log_callback("+ Начинаю извлечение аудио")  # type: ignore
        logging.info("Начинаю извлечение аудио")

        artist = info.get("uploader", "Unknown")
        title = info.get("title", "Unknown")

        actual_temp_path: Path = self._get_filepath(info)

        extension = actual_temp_path.suffix
        self._extension = extension

        self._safe_artist = re.sub(r'[<>:"/\\|?*]', "", str(artist))
        self._safe_title = re.sub(r'[<>:"/\\|?*]', "", str(title))

        filename = f"{self._safe_artist} - {self._safe_title}{extension}"
        logging.debug(f"Filename: {filename}")

        final_file_path: Path = output_folder / filename
        logging.debug(f"Final path: {final_file_path}")

        if final_file_path.exists():
            if actual_temp_path.exists():
                actual_temp_path.unlink()
            logging.warning(f"Файл {filename} уже существует")
            raise FileExistsError(f"Файл {filename} уже существует")

        try:
            if actual_temp_path.exists():
                actual_temp_path.replace(final_file_path)

                self.log_callback(f"+ Аудио сохранено как: {filename}")  # type: ignore
                logging.info(f"Аудио сохранено как: {filename}")

                file_size = final_file_path.stat().st_size
                logging.info(f"Файл скачан успешно. Размер: {file_size} байт")
            else:
                logging.error(f"Временный файл {actual_temp_path} не найден")
                raise FileNotFoundError(f"Временный файл {actual_temp_path} не найден")
        except FileNotFoundError as e:
            logging.error(f"Файл не найден: {e}")
            raise Exception(e)
        except Exception as e:
            logging.error(f"Критическая ошибка при сохранении трека: {e}")
            raise Exception(f"Критическая ошибка при сохранении трека: {e}")

        return final_file_path

    def add_tags(self, track_path: Path):

        self.log_callback("+ Начинаю добавление тегов")  # type: ignore
        logging.info("Начинаю добавление тегов")

        try:
            tags = EasyID3(track_path)
        except Exception as e:
            logging.error(f"Ошибка при чтении ID3 тегов: {e}")
            raise Exception(f"Ошибка при чтении ID3 тегов: {e}")

        tags["artist"] = self._safe_artist
        tags["title"] = self._safe_title
        tags.save(track_path)
        self.log_callback("+ Теги успешно добавлены")  # type: ignore
        logging.info("Теги успешно добавлены")

    def add_thumbnail(self, track_path: Path, thumbnail_url: str):
        self.log_callback("+ Начинаю добавление обложки")  # type: ignore
        logging.info("Начинаю добавление обложки")

        try:
            tags = ID3(track_path)
        except error:
            logging.error(
                "Ошибка при чтении ID3 тегов. Убедитесь, что файл существует и является MP3."
            )
            raise Exception(
                "Ошибка при чтении ID3 тегов. Убедитесь, что файл существует и является MP3."
            )

        try:
            response = requests.get(thumbnail_url, timeout=5)
            response.raise_for_status()
            thumbnail_data = response.content
        except requests.exceptions.RequestException as e:
            logging.error(
                f"Сетевая ошибка при загрузке обложки: {e}, URL: {thumbnail_url}"
            )
            raise RuntimeError(
                "Не удалось загрузить обложку из-за проблем с сетью"
            ) from e

        try:
            tags.add(
                APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc="Cover",
                    data=thumbnail_data,
                )
            )

            tags.save(track_path)
            logging.info("Обложка успешно добавлена")
            self.log_callback("+ Обложка успешно добавлена")  # type: ignore

        except Exception as e:
            logging.error(f"Не удалось добавить обложку в ID3 теги: {e}")
            raise Exception(f"Не удалось добавить обложку в ID3 теги: {e}")
