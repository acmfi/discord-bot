from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')

with open('src/token.txt', 'r') as token_file:
    TOKEN = token_file.read()

bot.load_extension(f'extensions.view.ban_hammer_view')

bot.run(TOKEN)
