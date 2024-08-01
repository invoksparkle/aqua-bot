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
    await clear_global_commands()
    await clear_guild_commands()

async def clear_global_commands():
    global_commands = await bot.tree.fetch_global_commands()
    for command in global_commands:
        await bot.tree.delete_global_command(command.id)
    print('Cleared all global commands.')

async def clear_guild_commands():
    for guild in bot.guilds:
        guild_commands = await bot.tree.fetch_guild_commands(guild.id)
        for command in guild_commands:
            await bot.tree.delete_guild_command(guild.id, command.id)
        print(f'Cleared all commands in guild: {guild.name}')

@bot.tree.command(name="hello", description="Say hello")
async def hello(ctx: discord.Interaction):
    await ctx.response.send_message('Hello!')

@bot.event
async def on_guild_join(guild):
    await clear_guild_commands()

bot.run(os.getenv('DISCORD_TOKEN'))
