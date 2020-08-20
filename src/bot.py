import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
TOKEN = open('src/token.txt', 'r').read()

bot.load_extension('Extensions.dynamic-channels')

@bot.event
async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')



bot.run(TOKEN)
