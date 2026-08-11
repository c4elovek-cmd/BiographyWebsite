import os
import json
import yt_dlp

# --- НАСТРОЙКИ ---
# Теперь здесь твоя верная ссылка
PLAYLIST_URL = 'https://soundcloud.com/c4elovechik/likes'

MUSIC_DIR = 'music'
OUTPUT_JSON = 'playlist.json'
ARCHIVE_FILE = 'downloaded_tracks.txt'

# Твой полный блэклист
BLACKLIST = [
    "Странный", "Её парень", "Священная война", "Плёнка", "грустинка",
    "xsonsss", "overdose", "ммм", "недотрога", "Chance", "фп", "флаг",
    "тинкер", "клановая", "ослепительна", "madk1d", "гимн", "Катюха",
    "попал", "MORGENSHTERN", "потеря"
]
# -----------------

def sync_tracks():
    print("-" * 50)
    print(f"1. Скачивание с {PLAYLIST_URL}...")
    print("-" * 50)
    
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{MUSIC_DIR}/%(title)s.%(ext)s',
        'download_archive': ARCHIVE_FILE,
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            {'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata', 'add_metadata': True}
        ],
        'ignoreerrors': True,
        'quiet': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([PLAYLIST_URL])
    except Exception as e:
        print(f"Ошибка при работе yt-dlp: {e}")

def update_playlist_json():
    print("\n" + "-" * 50)
    print("2. Генерация playlist.json...")
    print("-" * 50)
    
    playlist = []
    ignored_count = 0
    
    files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith('.mp3')]
    files.sort()

    for filename in files:
        name_lower = filename.lower()
        
        if any(bad_word.lower() in name_lower for bad_word in BLACKLIST):
            print(f"[БЛЭКЛИСТ] Пропущен: {filename}")
            ignored_count += 1
            continue

        playlist.append(filename)
        print(f"[ДОБАВЛЕНО] {filename}")

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(playlist, f, ensure_ascii=False, indent=2)
    
    print("-" * 50)
    print(f"Готово! В плейлисте: {len(playlist)} треков. Скрыто: {ignored_count}")

if __name__ == "__main__":
    sync_tracks()
    update_playlist_json()
