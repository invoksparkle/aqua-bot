import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready.')

@bot.slash_command(name="hello", description="Сказать привет")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Привет!")

bot.run(os.getenv('DISCORD_TOKEN'))
