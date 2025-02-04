import logging
import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN

# Минимизация логирования
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

extensions = ['bot.general', 'bot.youtube', 'bot.events']
for ext in extensions:
    bot.load_extension(ext)

bot.run(DISCORD_TOKEN)
