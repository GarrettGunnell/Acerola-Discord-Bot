#!/usr/bin/env python3

import discord
import random
import json
from collections import defaultdict

acerola_responses = ['nice', 'pog', 'damn that sucks', 'you should get some bitches', 'hell yeah', 'bro', 'bro...']
help_message = "\
```\n\
!help: \n\
\tDisplays the commands supported by the bot.\n\
\n\
!respond:\n\
\tSimulate a conversation with Acerola himself.\n\
\n\
!broboard:\n\
\tSee who has said bro the most in the server.\
```\
"

def def_value():
    return 0


bro_leaderboard = defaultdict(def_value)

TOKEN = open("token.txt","r").readline()

Intents = discord.Intents.default()
Intents.messages = True

client = discord.Client(intents = Intents)

@client.event
async def on_ready():
    print('Logged in')

@client.event
async def on_message(message):
    content = message.content.lower()
    user = str(message.author).split('#')[0]

    if message.author == client.user:
        return

    if content == '!help':
        await message.channel.send(help_message)
        return

    if content == '!respond':
        await message.channel.send(random.choice(acerola_responses))
        return

    if content == '!broboard':
        leaderboard = json.dumps(bro_leaderboard)[1:-1]

        await message.channel.send("```\n" + leaderboard + "\n```")
        return

    if 'bro' in content or 'vro' in content or 'bri' in content:
        bro_leaderboard[user] += 1

    
client.run(TOKEN)
