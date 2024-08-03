import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
from .utils import ffmpeg_options
from config.settings import GUILD_ID
import requests

ydl_opts = {
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

class YouTubeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def play(self, ctx: discord.ApplicationContext, url: str):
        """Воспроизвести аудио из видео на YouTube"""
        await ctx.defer()
        if ctx.author.voice is None:
            await ctx.respond("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
            return
        voice_channel = ctx.author.voice.channel

        vc = await voice_channel.connect()

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url2 = info['url']
                thumbnail_url = info.get('thumbnail', [{}])[0].get('url', '')
                if len(thumbnail_url) > 2048 or not thumbnail_url.startswith('http'):
                    thumbnail_url = 'https://img.youtube.com/vi/{}/default.jpg'.format(info['id'])

                source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
                vc.play(source)

                embed = discord.Embed(title="Сейчас играет", description=info['title'])
                embed.set_image(url=thumbnail_url)

                await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond("Произошла ошибка при попытке воспроизвести аудио.")
            raise e

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def stop(self, ctx: discord.ApplicationContext):
        """Остановить воспроизведение и отключиться от голосового канала"""
        vc = ctx.voice_client
        if vc and vc.is_playing():
            await vc.stop()
        if vc:
            await vc.disconnect()
        await ctx.respond("Остановлено и отключено от голосового канала.")

def setup(bot):
    bot.add_cog(YouTubeCommands(bot))
