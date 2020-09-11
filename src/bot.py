from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')

with open('src/token.txt', 'r') as token_file:
    TOKEN = token_file.read()

for file in os.listdir('src/funcionalidades'):
    if file.endswith('.py'):
        bot.load_extension(f'funcionalidades.{file[:-3]}')

bot.run(TOKEN)
