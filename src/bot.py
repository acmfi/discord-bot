import discord

client = discord.Client()
TOKEN = open('src/token.txt', 'r').read()
with open('src/blacklist_insultos.txt', 'r') as f:
    blacklist = [line.strip().casefold() for line in f if line.strip().casefold() != ""]


async def ban_word(message):
    word = message.content.split(" ", 1)[1]
    if word in blacklist: await message.channel.send("La palabra ya estaba baneada")
    else:
        with open("src/blacklist_insultos.txt", "a+") as file: file.write("\n" + word )
        file.close      
        blacklist.append(word)  
        await message.channel.send('Palabra censurada correctamente :)')    
        


async def unban_word(message):
    word = message.content.split(" ", 1)[1]
    if word in blacklist:     
        with open("src/blacklist_insultos.txt", "w") as file:
            for line in blacklist:
                if line.strip("\n") != word and line != "":
                    file.write("\n" + line )
        file.close
        blacklist.remove(word)  
        await message.channel.send('Palabra descensurada correctamente :)')  

    else:await message.channel.send("La palabra no está baneada, por lo que no se ha removido")
    



def check_role(person,role):  
    roles = [i.name for i in person.roles]      
    return role in roles



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):

    if message.author == client.user:
        return
    

    forbidden_words_used = [i for i in blacklist if i in message.content.casefold() and not message.content.startswith("/")] 

    if(len(forbidden_words_used)>0):         
        await message.delete() #Delete the message
        await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")  #Send a message on the same channel
        await message.author.send("El mensaje \n" + str(""f"```css\n{message.content}```""") + "no se ajusta a las normas, en los próximos mensajes no uses: " + str(forbidden_words_used).strip('[]') ) #Send a private message to the user



    if message.content.startswith('/censor') and len(message.content)>7:        
        if check_role(message.author,"Junta"): await ban_word(message)       
        else: await message.channel.send('Lo siento, no es nada personal, pero no tienes permiso para hacer eso :)')
        


    if message.content.startswith('/uncensor') and len(message.content)>9:                 
        if check_role(message.author,"Junta"): await unban_word(message)         
        else: await message.channel.send('Lo siento, no es nada personal, pero no tienes permiso para hacer eso :)')



    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



client.run(TOKEN)


