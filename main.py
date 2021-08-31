import discord
import random

TOKEN = open("token.txt","r").readline()

Intents = discord.Intents.default()
Intents.messages = True

client = discord.Client(intents = Intents)

@client.event
async def on_ready():
    print('Logged in')

acerola_responses = ['nice', 'pog', 'damn that sucks', 'you should get some bitches', 'hell yeah']

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!help':
        help_message = "\
        this is a help message \
        "

        await message.channel.send(help_message)
        return

    if message.content == '!respond':
        await message.channel.send(random.choice(acerola_responses))
        return

    

client.run(TOKEN)