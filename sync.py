import yt_dlp
import subprocess
import os
import json
import glob
from yt_dlp.utils import sanitize_filename

# Твоя ссылка на плейлист лайков
PLAYLIST_URL = 'https://soundcloud.com/c4elovechik/likes'
SAVE_DIR = 'music'

def filter_nested_playlists(info):
    playlist = info.get('playlist') or info.get('playlist_title') or ''
    if playlist and 'likes' not in playlist.lower():
        return f'Пропускаем (вложенный: {playlist})'
    return None

def sync_tracks():
    print("1. Скачиваю новые лайки...")
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    ydl_opts_dl = {
        'format': 'bestaudio/best',
        'outtmpl': f'{SAVE_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
        'download_archive': 'downloaded_tracks.txt',
        'match_filter': filter_nested_playlists 
    }
    with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
        ydl.download([PLAYLIST_URL])

    print("2. Проверяю удаленные лайки...")
    # Быстро получаем список названий только текущих лайков (без скачивания)
    ydl_opts_info = {
        'extract_flat': True,
        'quiet': True,
        'match_filter': filter_nested_playlists
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl_info:
        info = ydl_info.extract_info(PLAYLIST_URL, download=False)
        # Собираем список оригинальных названий треков
        liked_titles = [entry['title'] for entry in info.get('entries', []) if entry and entry.get('title')]
        
    # yt-dlp очищает спецсимволы при сохранении (например, убирает / или ?). 
    # Пропускаем названия через ту же самую очистку, чтобы они совпали с именами файлов.
    expected_files = [sanitize_filename(title) + '.mp3' for title in liked_titles]
    
    print("3. Сверяю файлы...")
    # Ищем файлы, которых больше нет в лайках
    for local_file in os.listdir(SAVE_DIR):
        if local_file.endswith('.mp3'):
            if local_file not in expected_files:
                file_path = os.path.join(SAVE_DIR, local_file)
                os.remove(file_path)
                print(f"[-] Удален трек (больше нет в лайках): {local_file}")

def update_playlist_json():
    print("4. Обновляю playlist.json...")
    # Собираем только файлы .mp3
    tracks = [os.path.basename(f) for f in glob.glob(f'{SAVE_DIR}/*.mp3')]
    
    # ОЧЕНЬ ВАЖНО: Принудительно задаем кодировку utf-8 и запрещаем 
    # преобразовывать русские буквы в "кракозябры" (ensure_ascii=False)
    # separators=(',', ':') делает файл компактным и убирает лишние пробелы, 
    # где может спрятаться ошибка.
    with open('playlist.json', 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=2, separators=(',', ': '))

def push_to_github():
    print("5. Отправляю изменения на GitHub...")
    try:
        # Флаг -A важен: он заставляет Git заметить не только новые, но и УДАЛЕННЫЕ файлы
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Зеркальная синхронизация лайков'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Готово! Сайт полностью синхронизирован.")
    except subprocess.CalledProcessError:
        print("Нет изменений для отправки.")

if __name__ == '__main__':
    sync_tracks()
    update_playlist_json()
    push_to_github()
