import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from .utils import ffmpeg_options, YouTubeUtils
from config.settings import GUILD_ID
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

class YouTubeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.volume = 0.5  # Начальный уровень громкости
        self.youtube_utils = YouTubeUtils()

    async def change_volume(self, ctx, change):
        if ctx.voice_client and ctx.voice_client.source:
            self.volume = max(0.0, min(2.0, self.volume + change))  # Ограничение громкости от 0% до 200%
            ctx.voice_client.source.volume = self.volume
            await ctx.respond(f"Громкость установлена на {int(self.volume * 100)}%")
        else:
            await ctx.respond("Бот не подключен к голосовому каналу или источник не поддерживает изменение громкости.")

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def play(self, ctx: discord.ApplicationContext, url: str):
        """Воспроизвести аудио из видео на YouTube"""
        await ctx.defer()
        if not ctx.author.voice:
            await ctx.respond("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
            return

        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()

        try:
            info = await self.bot.loop.run_in_executor(None, self.youtube_utils.extract_info, url)
            url2 = info['url']
            thumbnail_url = self.youtube_utils.get_thumbnail_url(info)

            embed = discord.Embed(title="Сейчас играет", description=info['title'])
            embed.set_image(url=thumbnail_url)

            view = self.create_volume_buttons()

            audio_source = FFmpegPCMAudio(url2, **ffmpeg_options)
            audio_source = PCMVolumeTransformer(audio_source, volume=self.volume)  # Поддержка громкости
            vc.play(audio_source, after=lambda e: self.bot.loop.create_task(self.disconnect_after_playback(vc)))
            await ctx.respond(embed=embed, view=view)
        except Exception as e:
            await ctx.respond(f"Произошла ошибка при попытке воспроизвести аудио. {str(e)}")
            raise e

    async def disconnect_after_playback(self, vc):
        if vc.is_connected():
            await vc.disconnect()

    def create_volume_buttons(self):
        volume_up = discord.ui.Button(style=discord.ButtonStyle.primary, label="🔊", custom_id="volume_up")
        volume_down = discord.ui.Button(style=discord.ButtonStyle.primary, label="🔉", custom_id="volume_down")

        async def volume_button_callback(interaction: discord.Interaction):
            change = 0.1 if interaction.custom_id == "volume_up" else -0.1
            await self.change_volume(interaction, change)
            await interaction.response.defer()

        volume_up.callback = volume_button_callback
        volume_down.callback = volume_button_callback

        view = discord.ui.View()
        view.add_item(volume_down)
        view.add_item(volume_up)
        return view

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def stop(self, ctx: discord.ApplicationContext):
        """Остановить воспроизведение и отключиться от голосового канала"""
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
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
