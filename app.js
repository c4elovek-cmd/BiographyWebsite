// --- СВГ ДЛЯ ЗВУКА ---
const svgMuted = `<svg viewBox="0 0 22 22" fill="none" class="vol-svg"><path d="M14 7.36979V6.40979C14 3.42979 11.93 2.28979 9.41 3.86979L6.49 5.69979C6.17 5.88979 5.8 5.99979 5.43 5.99979H4C2 5.99979 1 6.99979 1 8.99979V12.9998C1 14.9998 2 15.9998 4 15.9998H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path opacity="0.4" d="M9.41016 18.1302C11.9302 19.7102 14.0002 18.5602 14.0002 15.5902V11.9502" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path opacity="0.4" d="M17.81 8.41992C18.71 10.5699 18.44 13.0799 17 14.9999" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path opacity="0.4" d="M20.1501 6.7998C21.6201 10.2898 21.1801 14.3698 18.8301 17.4998" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 1L1 21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const svgUnmutedPlaying = `<svg viewBox="0 0 24 24" fill="none" class="vol-svg"><path d="M3.33008 9.99979V13.9998C3.33008 15.9998 4.33008 16.9998 6.33008 16.9998H7.76008C8.13008 16.9998 8.50008 17.1098 8.82008 17.2998L11.7401 19.1298C14.2601 20.7098 16.3301 19.5598 16.3301 16.5898V7.40979C16.3301 4.42979 14.2601 3.28979 11.7401 4.86979L8.82008 6.69979C8.50008 6.88979 8.13008 6.99979 7.76008 6.99979H6.33008C4.33008 6.99979 3.33008 7.99979 3.33008 9.99979Z" stroke="currentColor" stroke-width="1.5"/><path opacity="0.4" d="M19.3301 8C21.1101 10.37 21.1101 13.63 19.3301 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const svgUnmutedPaused = `<svg viewBox="0 0 24 24" fill="none" class="vol-svg"><path d="M5.5 9.99979V13.9998C5.5 15.9998 6.5 16.9998 8.5 16.9998H9.93C10.3 16.9998 10.67 17.1098 10.99 17.2998L13.91 19.1298C16.43 20.7098 18.5 19.5598 18.5 16.5898V7.40979C18.5 4.42979 16.43 3.28979 13.91 4.86979L10.99 6.69979C10.67 6.88979 10.3 6.99979 9.93 6.99979H8.5C6.5 6.99979 5.5 7.99979 5.5 9.99979Z" stroke="currentColor" stroke-width="1.5"/></svg>`;
// --- ЛОГИКА СЕКРЕТНЫХ ЛОГОВ ---
const adminLog = document.getElementById('admin-log');
function addLog(msg) {
if (window.location.hash === '#admin') { adminLog.style.display = 'block'; }
const time = new Date().toLocaleTimeString();
adminLog.innerHTML += `<div>[${time}] ${msg}</div>`;
adminLog.scrollTop = adminLog.scrollHeight;
}
window.addEventListener('hashchange', () => {
adminLog.style.display = (window.location.hash === '#admin') ? 'block' : 'none';
});
function moveOrbs() {
const orb1 = document.getElementById('orb1');
const orb2 = document.getElementById('orb2');
const maxX = window.innerWidth;
const maxY = window.innerHeight;
const randomX1 = Math.floor(Math.random() * maxX) - 150;
const randomY1 = Math.floor(Math.random() * maxY) - 150;
const randomX2 = Math.floor(Math.random() * maxX) - 150;
const randomY2 = Math.floor(Math.random() * maxY) - 150;
orb1.style.transform = `translate(${randomX1}px, ${randomY1}px) scale(${Math.random() * 0.5 + 0.8})`;
orb2.style.transform = `translate(${randomX2}px, ${randomY2}px) scale(${Math.random() * 0.5 + 0.8})`;
}
setTimeout(moveOrbs, 100);
setInterval(moveOrbs, 10000);
const expandBtn = document.getElementById('expand-btn');
const expandContent = document.getElementById('expand-content');
expandBtn.addEventListener('click', (e) => {
e.stopPropagation();
expandBtn.classList.toggle('active');
expandContent.classList.toggle('show');
});
const discordBtn = document.getElementById('discord-btn');
const discordText = document.getElementById('discord-text');
discordBtn.addEventListener('click', (e) => {
e.preventDefault();
navigator.clipboard.writeText('_c4elovek_').then(() => {
const originalText = discordText.innerText;
discordText.innerText = 'Скопировано!';
setTimeout(() => { discordText.innerText = originalText; }, 2000);
}).catch(err => addLog('Ошибка копирования: ' + err));
});
const BLACKLIST = [
"Странный", "Её парень", "Священная война", "Плёнка", "грустинка",
"xsonsss", "overdose", "ммм", "недотрога", "Chance", "фп", "флаг",
"тинкер", "клановая", "ослепительна", "madk1d", "гимн", "Катюха",
"попал", "MORGENSHTERN", "потеря", "truth yandere"
];
const audio = document.getElementById('bg-music');
const playBtn = document.getElementById('play-btn');
const iconPlay = document.getElementById('icon-play');
const iconPause = document.getElementById('icon-pause');
const statusText = document.getElementById('player-status');
const trackNameEl = document.getElementById('track-name');
const playlistMenu = document.getElementById('playlist-menu');
const togglePlaylistBtn = document.getElementById('toggle-playlist-btn');
// Звук
const volumeSlider = document.getElementById('volume-slider');
const volumeBtn = document.getElementById('volume-btn');
let lastVol = 0.7;
// Новые режимы воспроизведения
let isShuffle = false;
const shuffleBtn = document.getElementById('shuffle-btn');
const repeatBtn = document.getElementById('repeat-btn');
let playlist = [];
let currentTrackIndex = 0;
let hasStartedPlaying = false;
// Управление перемешиванием
shuffleBtn.addEventListener('click', (e) => {
e.stopPropagation();
isShuffle = !isShuffle;
shuffleBtn.classList.toggle('active', isShuffle);
addLog(`Режим 'Случайный трек': ${isShuffle ? 'ВКЛ' : 'ВЫКЛ'}`);
});
// Управление повтором (зацикливанием)
repeatBtn.addEventListener('click', (e) => {
e.stopPropagation();
audio.loop = !audio.loop; // Ставим или убираем loop на уровне аудиоэлемента
repeatBtn.classList.toggle('active', audio.loop);
addLog(`Режим 'Повтор трека': ${audio.loop ? 'ВКЛ' : 'ВЫКЛ'}`);
});
function updateVolumeIcon() {
if (audio.muted || audio.volume === 0) {
volumeBtn.innerHTML = svgMuted;
} else if (audio.paused) {
volumeBtn.innerHTML = svgUnmutedPaused;
} else {
volumeBtn.innerHTML = svgUnmutedPlaying;
}
}
volumeBtn.addEventListener('click', (e) => {
e.stopPropagation();
if (audio.muted || audio.volume === 0) {
audio.muted = false;
audio.volume = lastVol > 0 ? lastVol : 0.7;
volumeSlider.value = audio.volume;
} else {
lastVol = audio.volume;
audio.muted = true;
volumeSlider.value = 0;
}
updateVolumeIcon();
});
audio.volume = volumeSlider.value;
updateVolumeIcon();
volumeSlider.addEventListener('input', (e) => {
audio.volume = e.target.value;
if (audio.volume > 0) {
audio.muted = false;
lastVol = audio.volume;
}
updateVolumeIcon();
});
addLog("Получение playlist.json...");
fetch('playlist.json', { cache: 'no-store' })
.then(response => {
if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
return response.json();
})
.then(data => {
addLog(`Скачано треков из JSON: ${data.length}`);
playlist = data.filter(item => {
let fileName = typeof item === 'string' ? item : item.file;
const nameLower = fileName.toLowerCase();
return !BLACKLIST.some(badWord => nameLower.includes(badWord.toLowerCase()));
});
if(playlist.length > 0) {
addLog(`После фильтрации блэклистом осталось: ${playlist.length}`);
buildPlaylistMenu();
currentTrackIndex = Math.floor(Math.random() * playlist.length);
addLog(`Выбран рандомный трек: Индекс ${currentTrackIndex}`);
loadTrack(currentTrackIndex, false);
} else {
trackNameEl.innerText = "Плейлист пуст";
playlistMenu.innerHTML = '<div style="text-align:center; padding:15px; color:#a1a1aa;">Нет доступных треков</div>';
}
})
.catch(err => {
addLog(`КРИТИЧЕСКАЯ ОШИБКА: ${err.message}`);
trackNameEl.innerText = "Ошибка загрузки";
playlistMenu.innerHTML = `<div style="text-align:center; padding:15px; color:#ef4444;">Ошибка: ${err.message}</div>`;
});
function buildPlaylistMenu() {
playlistMenu.innerHTML = '';
playlist.forEach((item, index) => {
let fileName = typeof item === 'string' ? item : item.file;
let cleanName = (typeof item === 'object' && item.name) ? item.name : fileName.replace('.mp3', '').replace(/_/g, ' ');
let el = document.createElement('div');
el.className = 'playlist-item';
el.innerText = `${index + 1}. ${cleanName}`;
el.onclick = (e) => { e.stopPropagation(); loadTrack(index, true); playlistMenu.classList.remove('show'); };
playlistMenu.appendChild(el);
});
}
function loadTrack(index, autoPlay = true) {
currentTrackIndex = index;
let item = playlist[index];
let file = typeof item === 'string' ? item : item.file;
let defaultName = (typeof item === 'object' && item.name) ? item.name : file.replace('.mp3', '').replace(/_/g, ' ');
document.querySelectorAll('.playlist-item').forEach((el, i) => {
if(i === index) el.classList.add('active');
else el.classList.remove('active');
});
// Треки лежат в GitHub Releases (release tag: music), имена track01..track30
// по порядку playlist.json.
const fileUrl = 'https://github.com/c4elovek-cmd/BiographyWebsite/releases/download/music/track'
+ String(index + 1).padStart(2, '0') + '.mp3';
audio.src = fileUrl;
const absoluteUrl = new URL(fileUrl, window.location.href).href;
trackNameEl.innerText = defaultName;
statusText.innerText = "Чтение файла...";
addLog(`--------------------`);
addLog(`Загружаю файл: ${file}`);
if (window.jsmediatags) {
try {
window.jsmediatags.read(absoluteUrl, {
onSuccess: function(tag) {
let title = tag.tags.title || defaultName;
let artist = tag.tags.artist || 'c4elovek.online';
let artworkArray = [{ src: 'avatar.png', sizes: '512x512', type: 'image/png' }];
addLog(`Теги успешно прочитаны. Автор: "${artist}", Название: "${title}"`);
if (tag.tags.picture) {
addLog(`Обложка найдена внутри файла!`);
const data = tag.tags.picture.data;
const format = tag.tags.picture.format || 'image/jpeg';
const byteArray = new Uint8Array(data);
const blob = new Blob([byteArray], { type: format });
const imageUrl = URL.createObjectURL(blob);
artworkArray = [{ src: imageUrl, sizes: '512x512', type: format }];
} else {
addLog(`Обложка НЕ найдена, использую аватарку.`);
}
trackNameEl.innerText = title;
statusText.innerText = artist;
updateMediaSession(title, artist, artworkArray);
},
onError: function(error) {
addLog(`Ошибка чтения тегов: ${error.type || error.info || error}`);
trackNameEl.innerText = defaultName;
statusText.innerText = 'c4elovek.online';
updateMediaSession(defaultName, 'c4elovek.online', [{ src: 'avatar.png', sizes: '512x512', type: 'image/png' }]);
}
});
} catch (e) {
addLog(`Синхронная ошибка jsmediatags: ${e.message}`);
trackNameEl.innerText = defaultName;
statusText.innerText = 'c4elovek.online';
updateMediaSession(defaultName, 'c4elovek.online', [{ src: 'avatar.png', sizes: '512x512', type: 'image/png' }]);
}
} else {
addLog(`ОШИБКА: Библиотека jsmediatags не загружена!`);
trackNameEl.innerText = defaultName;
statusText.innerText = 'c4elovek.online';
updateMediaSession(defaultName, 'c4elovek.online', [{ src: 'avatar.png', sizes: '512x512', type: 'image/png' }]);
}
if(autoPlay) { togglePlay(true); }
updateVolumeIcon();
}
function updateMediaSession(title, artist, artwork) {
if ('mediaSession' in navigator) {
navigator.mediaSession.metadata = new MediaMetadata({
title: title,
artist: artist,
album: 'Избранный плейлист',
artwork: artwork
});
navigator.mediaSession.setActionHandler('play', () => togglePlay(true));
navigator.mediaSession.setActionHandler('pause', () => togglePlay(false));
navigator.mediaSession.setActionHandler('previoustrack', playPrevTrack);
navigator.mediaSession.setActionHandler('nexttrack', playNextTrack);
addLog(`Уведомление MediaSession обновлено.`);
}
}
function playNextTrack() {
if (playlist.length === 0) return;
if (isShuffle) {
let newIndex = currentTrackIndex;
if (playlist.length > 1) {
while (newIndex === currentTrackIndex) {
newIndex = Math.floor(Math.random() * playlist.length);
}
}
currentTrackIndex = newIndex;
} else {
currentTrackIndex++;
if (currentTrackIndex >= playlist.length) { currentTrackIndex = 0; }
}
addLog(`Переключение на СЛЕДУЮЩИЙ трек (Индекс: ${currentTrackIndex})`);
loadTrack(currentTrackIndex, true);
}
function playPrevTrack() {
if (playlist.length === 0) return;
currentTrackIndex--;
if (currentTrackIndex < 0) { currentTrackIndex = playlist.length - 1; }
addLog(`Переключение на ПРЕДЫДУЩИЙ трек (Индекс: ${currentTrackIndex})`);
loadTrack(currentTrackIndex, true);
}
togglePlaylistBtn.addEventListener('click', (e) => { e.stopPropagation(); playlistMenu.classList.toggle('show'); });
window.addEventListener('click', (e) => {
if (!playlistMenu.contains(e.target) && !togglePlaylistBtn.contains(e.target)) { playlistMenu.classList.remove('show'); }
if (!expandContent.contains(e.target) && !expandBtn.contains(e.target)) { expandContent.classList.remove('show'); expandBtn.classList.remove('active'); }
if (!hasStartedPlaying && audio.paused && playlist.length > 0 && !e.target.closest('button') && e.target !== volumeSlider) {
togglePlay(true);
hasStartedPlaying = true;
}
});
function togglePlay(forcePlay = false) {
if (playlist.length === 0) return;
const shouldPlay = typeof forcePlay === 'boolean' && forcePlay.isTrusted === undefined ? forcePlay : audio.paused;
if (shouldPlay) {
audio.play().then(() => {
iconPlay.style.display = 'none'; iconPause.style.display = 'block';
addLog("Воспроизведение начато.");
updateVolumeIcon();
}).catch(err => {
addLog(`АВТОЗАПУСК ЗАБЛОКИРОВАН браузером.`);
iconPlay.style.display = 'block'; iconPause.style.display = 'none';
updateVolumeIcon();
});
} else {
audio.pause(); iconPlay.style.display = 'block'; iconPause.style.display = 'none';
addLog("Плеер на паузе.");
updateVolumeIcon();
}
}
playBtn.addEventListener('click', (e) => { e.stopPropagation(); togglePlay(); hasStartedPlaying = true; });
audio.addEventListener('ended', playNextTrack);