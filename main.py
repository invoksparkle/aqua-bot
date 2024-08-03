import logging
import discord
from discord.ext import commands
from config.settings import DISCORD_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

extensions = ['bot.general', 'bot.youtube', 'bot.events']
for ext in extensions:
    bot.load_extension(ext)

bot.run(DISCORD_TOKEN)
