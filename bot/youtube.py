import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
from .utils import ffmpeg_options
from config.settings import GUILD_ID
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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
        self.volume = 0.5

    async def change_volume(self, ctx, change):
        if ctx.voice_client:
            self.volume = max(0.0, min(2.0, self.volume + change))
            ctx.voice_client.source.volume = self.volume
            await ctx.respond(f"Громкость установана на {int(self.volume * 100)}%")
        else:
            await ctx.respond("Бот не подключен к голосовому каналу.")

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
                if isinstance(info.get('thumbnails'), list):
                    thumbnails = sorted(info.get('thumbnails', []), key=lambda x: x.get('preference', -1), reverse=True)
                    thumbnail_url = next((t['url'] for t in thumbnails if t.get('url')), None)
                else:
                    thumbnail_url = None
                if not thumbnail_url or len(thumbnail_url) > 2048 or not thumbnail_url.startswith("http"):
                    thumbnail_url = f'https://img.youtube.com/vi/{info["id"]}/maxresdefault.jpg'
                embed = discord.Embed(title="Сейчас играет", description=info['title'])
                embed.set_image(url=thumbnail_url)

                volume_up = discord.ui.Button(style=discord.ButtonStyle.primary, label="🔊", custom_id="volume_up")
                volume_down = discord.ui.Button(style=discord.ButtonStyle.primary, label="🔉", custom_id="volume_down")

                async def volume_button_callback(interaction: discord.Interaction):
                    if interaction.custom_id == "volume_up":
                        await self.change_volume(ctx, 0.1)
                    elif interaction.custom_id == "volume_down":
                        await self.change_volume(ctx, -0.1)
                    await interaction.response.defer()

                volume_up.callback = volume_button_callback
                volume_down.callback = volume_button_callback

                view = discord.ui.View()
                view.add_item(volume_down)
                view.add_item(volume_up)

                audio_source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
                vc.play(audio_source)
                logger.info(f"Attempting to play URL: {url2}")
                await ctx.respond(embed=embed, view=view)
        except Exception as e:
            await ctx.respond(f"Произошла ошибка при попытке воспроизвести аудио. {str(e)}")
            raise e

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def stop(self, ctx: discord.ApplicationContext):
        """Остановить воспроизведение и отключиться от голосового канала"""
        vc = ctx.voice_client
        if vc:
            if vc.is_playing():
                vc.stop()
            await vc.disconnect()
            await ctx.respond("Остановлено и отключено от голосового канала.")
        else:
            await ctx.respond("Бот не подключен к голосовому каналу.")

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def volume_up(self, ctx: discord.ApplicationContext):
        """Увеличить громкость"""
        await self.change_volume(ctx, 0.1)

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def volume_down(self, ctx: discord.ApplicationContext):
        """Уменьшить громкость"""
        await self.change_volume(ctx, -0.1)


def setup(bot):
    bot.add_cog(YouTubeCommands(bot))
