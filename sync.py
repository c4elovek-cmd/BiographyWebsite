"""
sync.py v2 — полное обновление музыки плеера c4elovek.online

Что делает:
  1. Удаляет треки без обложек (битые качалки).
  2. Скачивает новые лайки со SoundCloud (yt-dlp + ffmpeg -> mp3).
  3. Заливает ВСЕ треки из папки music/ в GitHub Release "music"
     под именами track01.mp3..trackNN.mp3 (в алфавитном порядке).
  4. Генерирует playlist.json: [{"file": "trackNN.mp3", "name": "Красивое имя"}, ...]
  5. Пушит playlist.json в репозиторий -> Pages пердеплоится автоматически.

Запуск:  python sync.py            (полный цикл)
         python sync.py --no-download   (шаг 2 пропустить)

Требования: pip install yt_dlp mutagen; ffmpeg (путь ниже); gh CLI (авторизован).
Запускать из папки, где лежит этот файл (рядом должны быть music/ и playlist.json).
"""

import json, os, sys, base64, subprocess, urllib.request, urllib.parse

# ---------------- НАСТРОЙКИ ----------------
REPO = "c4elovek-cmd/BiographyWebsite"
TAG = "music"
MUSIC_DIR = "music"
OUTPUT_JSON = "playlist.json"
GH_EXE = r"G:\Users\c4elovek\.zcode\workspace\default\gh-cli\bin\gh.exe"  # gh CLI с авторизацией
FFMPEG_DIR = r"G:\Users\c4elovek\.zcode\workspace\default\tools\ffmpeg\ffmpeg-master-latest-win64-gpl\bin"
PLAYLIST_URL = "https://soundcloud.com/c4elovechik/likes"

BLACKLIST = [
    "Странный", "Её парень", "Священная война", "Плёнка", "грустинка",
    "xsonsss", "overdose", "ммм", "недотрога", "Chance", "фп", "флаг",
    "тинкер", "клановая", "ослепительна", "madk1d", "гимн", "Катюха",
    "попал", "MORGENSHTERN", "потеря", "truth yandere"
]
# -------------------------------------------

NO_DOWNLOAD = "--no-download" in sys.argv


def gh_token():
    return subprocess.run([GH_EXE, "auth", "token"], capture_output=True,
                          text=True).stdout.strip()


def api_release_list():
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases?per_page=100",
        headers={"Authorization": "token " + gh_token(), "User-Agent": "curl/8"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def step_cover_cleanup():
    print("-" * 50)
    print("0. Проверка обложек...")
    from mutagen.mp3 import MP3
    if not os.path.exists(MUSIC_DIR):
        return
    deleted = 0
    for filename in os.listdir(MUSIC_DIR):
        if not filename.lower().endswith(".mp3"):
            continue
        filepath = os.path.join(MUSIC_DIR, filename)
        has_cover = False
        try:
            audio = MP3(filepath)
            if audio.tags:
                has_cover = any(str(k).startswith("APIC") for k in audio.tags.keys())
        except Exception:
            pass
        if not has_cover:
            print("  [УДАЛЁН] нет обложки:", filename)
            os.remove(filepath)
            deleted += 1
    print(f"  Удалено: {deleted}")


def step_download():
    print("-" * 50)
    print("1. Скачивание новых лайков со SoundCloud...")
    import yt_dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{MUSIC_DIR}/%(title)s.%(ext)s",
        "writethumbnail": False,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            {"key": "FFmpegMetadata", "add_metadata": True},
        ],
        "ignoreerrors": True,
        "quiet": False,
        "nooverwrites": True,
        "ffmpeg_location": FFMPEG_DIR,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([PLAYLIST_URL])
    except Exception as e:
        print("  yt-dlp ошибка (продолжаю с существующими файлами):", e)


def build_tracks():
    files = sorted(f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3"))
    tracks = []
    for i, filename in enumerate(files, start=1):
        name_lower = filename.lower()
        if any(bad.lower() in name_lower for bad in BLACKLIST):
            print("  [БЛЭКЛИСТ]", filename)
            continue
        pretty = filename[:-4].replace("_", " ")
        tracks.append({"file": f"track{i:02d}.mp3", "name": pretty, "_src": filename})
    return tracks


def step_release_upload(tracks):
    print("-" * 50)
    print("2. Обновление GitHub Release '" + TAG + "'...")
    token = gh_token()
    rel = None
    for r0 in api_release_list():
        if r0["tag_name"] == TAG:
            rel = r0
            break
    if not rel:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/releases",
            headers={"Authorization": "token " + token, "User-Agent": "curl/8",
                     "Content-Type": "application/json"},
            data=json.dumps({"tag_name": TAG, "target_commitish": "main",
                             "name": "Музыка плеера",
                             "body": "trackNN.mp3 по порядку playlist.json"}).encode(),
            method="POST")
        rel = json.loads(urllib.request.urlopen(req, timeout=30).read())
    rel_id = rel["id"]
    assets = json.loads(urllib.request.urlopen(
        f"https://api.github.com/repos/{REPO}/releases/{rel_id}/assets?per_page=100").read())

    # удаляем старые trackNN-ассеты
    for a in assets:
        if a["name"].startswith("track") and a["name"].endswith(".mp3"):
            req = urllib.request.Request(
                f"https://api.github.com/repos/{REPO}/releases/assets/{a['id']}",
                headers={"Authorization": "token " + token, "User-Agent": "curl/8"}, method="DELETE")
            urllib.request.urlopen(req, timeout=30)
    print("  старые ассеты удалены")

    for t in tracks:
        local = os.path.join(MUSIC_DIR, t["_src"])
        quoted = urllib.parse.quote(t["file"])
        r = subprocess.run([
            "curl", "-s", "--max-time", "600",
            "-H", "Authorization: token " + token,
            "-H", "Content-Type: application/octet-stream",
            "-T", local,
            f"https://uploads.github.com/repos/{REPO}/releases/{rel_id}/assets?name={quoted}",
        ], capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(f"upload fail {t['file']}")
        print("  [OK]", t["file"], "<-", t["name"])


def step_playlist(tracks):
    print("-" * 50)
    print("3. Генерация playlist.json...")
    out = [{"file": t["file"], "name": t["name"]} for t in tracks]
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  Треков в плейлисте: {len(out)}")


def step_push_playlist():
    print("-" * 50)
    print("4. Пуш playlist.json в репозиторий...")
    content = open(OUTPUT_JSON, "rb").read()
    payload = {"message": "sync: update playlist", "content": base64.b64encode(content).decode()}
    r = subprocess.run([GH_EXE, "api", f"repos/{REPO}/contents/playlist.json", "-q", ".sha"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode == 0 and r.stdout.strip():
        payload["sha"] = r.stdout.strip()
    pp = "push_tmp.json"
    open(pp, "w", encoding="utf-8").write(json.dumps(payload))
    r = subprocess.run([GH_EXE, "api", "--method", "PUT",
                        f"repos/{REPO}/contents/playlist.json", "--input", pp],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError("push fail: " + r.stderr[:200])
    d = json.loads(r.stdout)
    print("  pushed, commit", d["commit"]["sha"][:10], "- Pages задеплоит сам")
    os.remove(pp)


if __name__ == "__main__":
    step_cover_cleanup()
    if not NO_DOWNLOAD:
        step_download()
    else:
        print("(шаг скачивания пропущен: --no-download)")
    tracks = build_tracks()
    step_release_upload(tracks)
    step_playlist(tracks)
    step_push_playlist()
    print("\nГОТОВО. Pages задеплоит изменения автоматически (~2 мин).")
