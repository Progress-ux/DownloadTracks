# YouTube Tracks Downloader

Универсальный инструмент для скачивания аудио из YouTube с поддержкой тегов и обложек. 
Одно ядро — два интерфейса.

## Особенности
- **GUI**: Удобное окно на PySide6.
- **CLI**: Быстрый консольный интерфейс с интерактивным меню.
- **Авто-теги**: Заполнение Артиста и Названия, вшивка обложки.
- **Гибкость**: Настройка качества и форматов (mp3, opus, flac и др.).

## Установка

1. **Создание окружения:**

```bash
python -m venv venv
source ./venv/bin/activate # Для Linux/Arch
# venv\Scripts\activate    # Для Windows
```

2. **Установка зависимостей:**

Для полной версии (GUI + CLI):
```bash
pip install -r requirements.txt
```

Только для консольной версии:
```bash
pip install -r requirements-cli.txt
```

3. **Установка ffmpeg:**

### Arch
```bash
sudo pacman -S ffmpeg
```

### Ubuntu/Debian:
``` bash
sudo apt update
sudo apt install ffmpeg
```

### macOS:
``` bash
brew install ffmpeg
```

### Windows:
* Скачайте FFmpeg с [официального сайта](https://ffmpeg.org/download.html)
* Добавьте путь к FFmpeg в переменную окружения PATH, либо добавьте путь в `config.json`:
  
```json
"ffmpeg_location": "путь/к/бинарнику/ffmpeg"
```
  
## Запуск
### Графический интерфейс (GUI)

```bash
python main_gui.py
```

### Консольный интерфейс (CLI)

```bash
python main_cli.py
```

## Использование

Программа поддерживает любые стандартные ссылки YouTube:

- ✅ `https://www.youtube.com/watch?v=...`
- ✅ `https://youtu.be/...`
- ✅ Ссылки с параметрами плейлистов (скачивается только выбранный трек).
  
## Структура проекта

- `core/` — логика загрузки и обработки (не зависит от UI).
- `infrastructure/` — работа с конфигами и файловой системой.
- `ui/` — файлы графического интерфейса.