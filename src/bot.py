import discord
from discord.ext import commands
import os


bot = commands.Bot(command_prefix='¡')

TOKEN = open('token.txt', 'r').read()


for file in os.listdir('./funcionalidades'):
    if file.endswith('.py'):
        bot.load_extension(f'funcionalidades.{file[:-3]}')


bot.run(TOKEN)
