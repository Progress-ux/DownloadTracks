import os
import re
from config import Config
from video_download import VideoDownloader

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
      raise Exception("Ссылки не введены")

   unique_list = list(dict.fromkeys(urls))

   return unique_list

def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def main():
   config = Config()
   create_output_folder(config.config.get("output", "downloads"))

   try:
      urls = enter_urls()
   except Exception as e:
      print(e)
      return
   
   video_downloader = VideoDownloader()

   for i, url in enumerate(urls, start=1):
      try:
         output_dir = config.config.get("output", "downloads")
         info = video_downloader.download_track(
            url.strip(), 
            config.yt_dlp_config_data, 
            i,
            outtmpl=os.path.join(output_dir, "temp.%(ext)s")
         )

         video_downloader.save_track(
            info, 
            output_dir
         )

         filename = f"{video_downloader.get_safe_artist()} - {video_downloader.get_safe_title()}.mp3"
         track_path = os.path.join(output_dir, filename)

         video_downloader.add_tags(track_path)

         video_downloader.add_thumbnail(
            track_path,
            str(info.get("thumbnail", ""))
         )
         print(f"Загрузка {filename} завершена")

      except FileExistsError as e:
         print(f"Пропуск: {e}")
      
      except Exception as e:
         print(f"❌ Ошибка при загрузке {url}: {e}")
         continue

if __name__ == "__main__":
    main()