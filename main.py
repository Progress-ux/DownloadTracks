import os
import re
import yt_dlp
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT, APIC
from tqdm import tqdm

# ===== Получение текста песни (опционально) =====
def get_lyrics(title: str, artist: str):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and "lyrics" in r.json():
            return r.json()["lyrics"]
    except:
        pass
    return None

# ===== Прогрессбар =====
pbar = None
def progress_hook(d):
    global pbar
    if d["status"] == "downloading":
        if pbar is None:
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            pbar = tqdm(total=total, unit="B", unit_scale=True, desc="Downloading")
        pbar.update(d["downloaded_bytes"] - pbar.n)
    elif d["status"] == "finished":
        if pbar:
            pbar.close()
            pbar = None
            print("✅ Загрузка завершена")

# ===== Скачивание аудио =====
def download_audio(url, out_dir="downloads"):
    os.makedirs(out_dir, exist_ok=True)

    temp_template = f"{out_dir}/temp.%(ext)s"
    temp_template = f"{out_dir}/temp.%(ext)s"
    node_path = r"C:\Program Files\nodejs" 
    os.environ["PATH"] += os.pathsep + node_path
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": temp_template,
        "progress_hooks": [progress_hook],
        "quiet": False,
        "noprogress": True,
        #"cookiesfrombrowser": ("firefox", r"C:\Users\user\AppData\Roaming\zen\Profiles\iv14k5xb.Default (release)"),
        "extractor_args": {
            "youtube": {
                "player_client": ["web", "android",],
            }
        },
        "javascript_executor": "node",
        "ffmpeg_location": r"C:\ffmpeg\bin\ffmpeg.exe",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    # Название файла
    artist = info.get("uploader", "Unknown")
    title = info.get("title", "Unknown")

    safe_artist = re.sub(r'[<>:"/\\|?*]', "", artist)
    safe_title = re.sub(r'[<>:"/\\|?*]', "", title)

    final_name = f"{out_dir}/{safe_artist} - {safe_title}.mp3"
    os.rename(f"{out_dir}/temp.mp3", final_name)

    # Заполнение тегов
    try:
        audio = EasyID3(final_name)
    except:
        audio = EasyID3()
        audio.save(final_name)

    audio["title"] = title
    audio["artist"] = artist
    audio["album"] = artist
    audio.save()

    tags = ID3(final_name)

    # Лирика
    lyrics = get_lyrics(title, artist)
    if lyrics:
        tags.add(USLT(encoding=3, desc="Lyrics", text=lyrics))

    # Обложка
    thumb_url = info.get("thumbnail")
    if thumb_url:
        try:
            img = requests.get(thumb_url, timeout=5).content
            tags.add(
                APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,  # обложка передняя
                    desc="Cover",
                    data=img,
                )
            )
            print("🖼 Обложка добавлена")
        except Exception as e:
            print(f"⚠️ Ошибка загрузки обложки: {e}")

    tags.save(final_name)

    return final_name

# ===== Основной запуск =====
def main():
    print("Вставь ссылки на YouTube (через пробел, запятую или построчно).")
    print("Окончание ввода — пустая строка.\n")

    urls = []
    while True:
        line = input()
        if not line.strip():
            break
        urls.extend(re.split(r"[ ,]+", line.strip()))

    if not urls:
        print("❌ Ссылки не введены")
        return
    i = 0
    for url in urls:
        i += 1 
        if not url.strip():
            continue
        print(f"\n{i}.🎵 Скачиваю: {url}")
        try:
            file = download_audio(url.strip())
            print(f"➡️ Сохранено: {file}")
        except Exception as e:
            print(f"❌ Ошибка при загрузке {url}: {e}")

if __name__ == "__main__":
    main()
