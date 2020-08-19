from discord.ext import commands

bot = commands.Bot(command_prefix='!')
TOKEN = open('token.txt', 'r').read()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.load_extension('Extensions.voice_control')
bot.run(TOKEN)
