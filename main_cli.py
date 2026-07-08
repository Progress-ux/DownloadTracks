from pathlib import Path

from infrastructure.config_manager import Config
from core.downloader import VideoDownloader
from core.video_processor import VideoProcessor
from core.yt_dlp_logger import NoWarningLogger
import re
import logging
import argparse


def main_menu():
    print("\n=== YouTube Music Downloader (CLI) ===")
    print("1. Скачать один или несколько треков (ввод вручную)")
    print("2. Настройки (посмотреть текущие)")
    print("0. Выход")
    return input("\nВыберите действие: ")


def enter_urls():
    print("Вставь ссылки на YouTube (через пробел, запятую или построчно).")
    print("Окончание ввода — пустая строка.\n")

    urls = []
    while True:
        line = input()
        if not line.strip():
            break
        urls.extend(re.split(r"[ ,]+", line.strip()))

    if not urls:
        logging.error("Ссылки не введены")
        raise Exception("Ссылки не введены")

    unique_list = list(dict.fromkeys(urls))

    return unique_list


def print_yt_dlp_config(config):
    print("\nТекущие настройки yt-dlp:")
    for key, value in config.config.get("yt-dlp-config", {}).items():
        print(f"  {key}: {value}")
    input("\nНажмите Enter, чтобы вернуться в главное меню...")


def create_output_folder(output_folder: Path):
    if not output_folder.exists():
        output_folder.mkdir(parents=True, exist_ok=True)


def draw_progress_bar(progress):
    bar_length = 50
    filled_length = int(bar_length * progress // 100)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\rЗагрузка: |{bar}| {progress}%", end="\r", flush=True)

    if progress >= 100:
        print()  # Move to a new line after loading is complete


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()
    log_mode = logging.DEBUG

    if not args.debug:
        log_mode = logging.INFO

    filename_log = Path.home() / ".local/state/DownloadTrack/download.log"
    filename_log.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=log_mode,
        filename=filename_log,
        encoding="utf-8",
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    )

    config_path = Path.home() / ".config/DownloadTracks/config.json"
    print(config_path)
    config = Config(path_config=config_path)
    config.config["yt-dlp-config"]["logger"] = NoWarningLogger(logging.error)

    output_dir = Path(config.config["output"])
    create_output_folder(output_dir)

    downloader = VideoDownloader(
        log_callback=print, progress_callback=draw_progress_bar
    )

    video_processor = VideoProcessor(log_callback=print)

    try:
        while True:
            choice = main_menu()

            if choice == "1":
                urls = enter_urls()
                for i, url in enumerate(urls, start=1):
                    try:

                        info = downloader.download_track(
                            url.strip(),
                            config.config.get("yt-dlp-config", {}),
                            i,
                            outtmpl=output_dir / "temp.%(ext)s",
                        )

                        filepath: Path = video_processor.save_track(info, output_dir)

                        filename = f"{video_processor.get_safe_artist()} - {video_processor.get_safe_title()}{video_processor.get_extension()}"

                        video_processor.add_tags(filepath)
                        video_processor.add_thumbnail(
                            filepath, str(info.get("thumbnail", ""))
                        )

                        logging.info(f"Загрузка {filename} завершена")
                        print(f"+ Загрузка {filename} завершена")

                    except FileExistsError as e:
                        print(f"- Пропуск: {e}")
                        logging.warning(f"Пропуск: {e}")
                        continue
                    except Exception as e:
                        logging.error(f"Ошибка при загрузке {url}: {e}")
                        print(f"- Ошибка при загрузке {url}: {e}")
                        continue

            elif choice == "2":
                print("\nТекущие настройки:")
                print(f"Выходная папка: {config.config.get('output', 'downloads')}")
                print_yt_dlp_config(config)

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")


main()
