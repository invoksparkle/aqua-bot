import os
import logging
import discord
from discord.ext import commands
import youtube_dl

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

# Получение ID гильдии из переменной окружения
GUILD_ID = os.getenv('GUILD_ID')
if GUILD_ID is None:
    raise ValueError("Переменная окружения GUILD_ID не установлена")
GUILD_ID = int(GUILD_ID)

# Настройка youtube_dl
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

@bot.event
async def on_ready():
    logger.info(f'Бот {bot.user} готов.')

# Гильдейская команда
@bot.slash_command(guild_ids=[GUILD_ID])
async def hello(ctx: discord.ApplicationContext):
    """Поздороваться с ботом"""
    await ctx.respond(f"Привет, {ctx.author}!")

@bot.slash_command(guild_ids=[GUILD_ID])
async def play(ctx: discord.ApplicationContext, url: str):
    """Воспроизвести аудио из видео на YouTube"""
    await ctx.defer()
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.respond("Вы должны быть в голосовом канале, чтобы использовать эту команду.")
        return
    
    vc = await voice_channel.connect()
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
        vc.play(source)
    
    await ctx.respond(f"Воспроизведение: {url}")

@bot.slash_command(guild_ids=[GUILD_ID])
async def stop(ctx: discord.ApplicationContext):
    """Остановить воспроизведение и отключиться от голосового канала"""
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.stop()
    if vc:
        await vc.disconnect()
    await ctx.respond("Остановлено и отключено от голосового канала.")

bot.run(os.getenv('DISCORD_TOKEN'))
