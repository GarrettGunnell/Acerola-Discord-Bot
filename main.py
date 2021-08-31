import discord
import random

acerola_responses = ['nice', 'pog', 'damn that sucks', 'you should get some bitches', 'hell yeah', 'bro', 'bro...']
help_message = "\
```\n\
!help: \n\
\tDisplays the commands supported by the bot.\n\
\n\
!respond:\n\
\tSimulate a conversation with Acerola himself.\n\
```\
"

TOKEN = open("token.txt","r").readline()

Intents = discord.Intents.default()
Intents.messages = True

client = discord.Client(intents = Intents)

@client.event
async def on_ready():
    print('Logged in')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!help':
        await message.channel.send(help_message)
        return

    if message.content == '!respond':
        await message.channel.send(random.choice(acerola_responses))
        return

    
client.run(TOKEN)