from yt_dlp import YoutubeDL

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

class YouTubeUtils:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noprogress': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
        }

    def extract_info(self, url):
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            return info

    def get_thumbnail_url(self, info):
        if isinstance(info.get('thumbnails'), list):
            thumbnails = sorted(info.get('thumbnails', []), key=lambda x: x.get('preference', -1), reverse=True)
            thumbnail_url = next((t['url'] for t in thumbnails if t.get('url')), None)
        else:
            thumbnail_url = None
        if not thumbnail_url or len(thumbnail_url) > 2048 or not thumbnail_url.startswith("http"):
            thumbnail_url = f'https://img.youtube.com/vi/{info["id"]}/maxresdefault.jpg'
        return thumbnail_url
