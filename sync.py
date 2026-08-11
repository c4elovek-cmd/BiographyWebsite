import os
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

# --- Настройки ---
MUSIC_DIR = 'music'
COVERS_DIR = os.path.join(MUSIC_DIR, 'covers')
OUTPUT_JSON = 'playlist.json'

BLACKLIST = [
    'chainsaww',
    'overdose',
    'tesla'
]
# -----------------

def update_playlist():
    print("-" * 40)
    print("Синхронизация музыки и обложек...")
    
    # Создаем папку для обложек, если её нет
    if not os.path.exists(COVERS_DIR):
        os.makedirs(COVERS_DIR)

    playlist = []
    
    # Ищем mp3 файлы
    files = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith('.mp3')]
    files.sort()

    for filename in files:
        name_lower = filename.lower()
        
        # Проверка блэклиста
        if any(bad_word in name_lower for bad_word in BLACKLIST):
            print(f"[ПРОПУСК] {filename}")
            continue

        filepath = os.path.join(MUSIC_DIR, filename)
        cover_filename = None

        # Пытаемся вытащить обложку (APIC тег)
        try:
            audio = MP3(filepath, ID3=ID3)
            if audio.tags:
                for tag in audio.tags.values():
                    if tag.FrameID == 'APIC':
                        # Генерируем имя для картинки
                        cover_filename = filename.replace('.mp3', '.jpg')
                        cover_path = os.path.join(COVERS_DIR, cover_filename)
                        
                        # Сохраняем картинку
                        with open(cover_path, 'wb') as img:
                            img.write(tag.data)
                        break
        except Exception as e:
            print(f"[ОШИБКА] Чтение тегов {filename}: {e}")

        # Добавляем трек в JSON как объект
        playlist.append({
            "file": filename,
            "cover": f"music/covers/{cover_filename}" if cover_filename else None
        })
        
        print(f"[ДОБАВЛЕНО] {filename}" + (" (+обложка)" if cover_filename else ""))

    # Сохраняем playlist.json
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(playlist, f, ensure_ascii=False, indent=2)
    
    print("-" * 40)
    print("Готово! playlist.json обновлен.")

if __name__ == "__main__":
    update_playlist()
