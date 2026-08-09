import yt_dlp
import subprocess
import os
import json
import glob

PLAYLIST_URL = 'https://soundcloud.com/c4elovechik/likes'
SAVE_DIR = 'music'

def download_tracks():
    print("Начинаю загрузку треков...")
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{SAVE_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ignoreerrors': True,
        'download_archive': 'downloaded_tracks.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([PLAYLIST_URL])

def update_playlist_json():
    print("Генерация playlist.json...")
    tracks = []
    # Ищем все mp3 файлы в папке music
    for file in glob.glob(f'{SAVE_DIR}/*.mp3'):
        tracks.append(os.path.basename(file))
    
    # Сохраняем список в JSON файл
    with open('playlist.json', 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False)

def push_to_github():
    print("Отправка файлов на GitHub...")
    try:
        subprocess.run(['git', 'add', f'{SAVE_DIR}/', 'downloaded_tracks.txt', 'playlist.json'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Авто-обновление музыки'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Треки успешно загружены!")
    except subprocess.CalledProcessError:
        print("Нет новых изменений для отправки.")

if __name__ == '__main__':
    download_tracks()
    update_playlist_json()
    push_to_github()
