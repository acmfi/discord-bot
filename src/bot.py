import discord

client = discord.Client()
TOKEN = open('src/token.txt', 'r').read()
with open('src/blacklist_insultos.txt', 'r') as f:
    blacklist = [line.strip().casefold() for line in f]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #for(i in blacklist): if i in message.content: print("------------")
    for i in blacklist:
         if(i in message.content.casefold()):            
            await message.delete()
            await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")
            #await message.author.send("El mensaje \n" + message.content + "\nno se ajusta a las normas, la palabra " + i + " está prohibida")
            await message.author.send("El mensaje \n" + str(""f"```css\n{message.content}```""") + "no se ajusta a las normas, la palabra " + i + " está prohibida")
        
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



client.run(TOKEN)

str("""```css\nThis is some colored Text```""")
