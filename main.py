#!/usr/bin/env python3

import discord
import random
import json
from collections import defaultdict

acerola_responses = ['nice', 'pog', 'damn that sucks', 'you should get some bitches', 'hell yeah', 'bro', 'bro...', 'kino', 'I love people like you', 
'No\n https://tenor.com/view/keanu-reeves-john-wick-awesome-gif-18042382', ':eyes:', 'I love Molly Rankin', 'peep my story', 'listen to song',
'cringe', 'based']
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

def def_dict():
    return defaultdict(def_value)

bro_leaderboard = defaultdict(def_dict)

with open('broboard.txt') as json_file:
    bro_data = json.load(json_file)
    for key in bro_data.keys():
        for key2, value in bro_data[key].items():
            bro_leaderboard[key][key2] = value


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
    server = str(message.guild)

    if message.author == client.user:
        return

    if content == '!help':
        await message.channel.send(help_message)
        return

    if content == '!respond':
        responses = random.sample(acerola_responses, 4)
        await message.channel.send(random.choice(responses))
        return

    if content == '!broboard':
        sorted_leaderboard = sorted(bro_leaderboard[server].items(), key = lambda x: x[1], reverse=True)
        sorted_leaderboard = sorted_leaderboard[0:25]
        
        leaderboard_string = f"```markdown\n"
        for i in range(0, len(sorted_leaderboard)):
            leaderboard_string += f"#{i + 1} {sorted_leaderboard[i][0]}: {sorted_leaderboard[i][1]}\n"
        leaderboard_string += f"\n```"

        await message.channel.send(leaderboard_string)
        return

    if 'bro' in content or 'vro' in content or 'bri' in content:
        bro_leaderboard[server][user] += 1
        with open('broboard.txt', 'w') as outfile:
            json.dump(bro_leaderboard, outfile)

    
client.run(TOKEN)
