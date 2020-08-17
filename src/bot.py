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
    
    for i in blacklist:
         if(i in message.content.casefold()):            
            await message.delete() #Delete the message
            await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")  #Send a message on the same channel
            await message.author.send("El mensaje \n" + str(""f"```css\n{message.content}```""") + "no se ajusta a las normas, la palabra " + i + " está prohibida") #Send a private message to the user
        
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



client.run(TOKEN)


