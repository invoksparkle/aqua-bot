import os
import discord
from discord import Intents
from discord.ext import commands

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready.')

async def clear_slash_commands():
    for guild in bot.guilds:
        commands = await bot.http.get_guild_application_commands(bot.user.id, guild.id)
        for command in commands:
            await bot.http.delete_guild_application_command(bot.user.id, guild.id, command['id'])
        print(f'Cleared all slash commands in guild: {guild.name}')

@bot.slash_command(name="hello", description="Say hello")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond('Hello!')

@bot.event
async def on_guild_join(guild):
    await clear_slash_commands()

bot.loop.create_task(clear_slash_commands())
bot.run(os.getenv('DISCORD_TOKEN'))
