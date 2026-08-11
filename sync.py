import os
import json
import yt_dlp
from mutagen.mp3 import MP3

# --- НАСТРОЙКИ ---
PLAYLIST_URL = 'https://soundcloud.com/c4elovechik/likes'

MUSIC_DIR = 'music'
OUTPUT_JSON = 'playlist.json'

# Обновленный блэклист
BLACKLIST = [
    "Странный", "Её парень", "Священная война", "Плёнка", "грустинка",
    "xsonsss", "overdose", "ммм", "недотрога", "Chance", "фп", "флаг",
    "тинкер", "клановая", "ослепительна", "madk1d", "гимн", "Катюха",
    "попал", "MORGENSHTERN", "потеря", "truth yandere"
]
# -----------------

def clean_coverless_tracks():
    print("-" * 50)
    print("0. Проверка треков на наличие обложек...")
    if not os.path.exists(MUSIC_DIR):
        return
        
    deleted_count = 0
    for filename in os.listdir(MUSIC_DIR):
        if filename.lower().endswith('.mp3'):
            filepath = os.path.join(MUSIC_DIR, filename)
            has_cover = False
            try:
                audio = MP3(filepath)
                if audio.tags:
                    for key in audio.tags.keys():
                        if key.startswith('APIC'):
                            has_cover = True
                            break
            except Exception:
                pass # Пропускаем битые файлы
            
            if not has_cover:
                print(f"[УДАЛЕНИЕ] Нет обложки, файл удален для перекачки: {filename}")
                os.remove(filepath)
                deleted_count += 1
                
    if deleted_count > 0:
        print(f"Итого удалено для обновления: {deleted_count} треков.")
    else:
        print("Все скачанные треки имеют вшитые обложки.")

def sync_tracks():
    print("-" * 50)
    print(f"1. Скачивание новых треков с {PLAYLIST_URL}...")
    print("-" * 50)
    
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    # Убрали download_archive, чтобы yt-dlp проверял наличие самих файлов.
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{MUSIC_DIR}/%(title)s.%(ext)s',
        'writethumbnail': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            {'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata', 'add_metadata': True}
        ],
        'ignoreerrors': True,
        'quiet': False,
        'nooverwrites': True # Пропускает треки, которые УЖЕ есть в папке
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
    clean_coverless_tracks()
    sync_tracks()
    update_playlist_json()
