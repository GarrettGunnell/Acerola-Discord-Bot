#!/usr/bin/env python3

import discord
import random
import time
import json
from collections import defaultdict
import tweepy
import threading
from dotenv import load_dotenv
from os import environ
load_dotenv()

acerola_responses = ['nice', 'pog', 'damn that sucks', 'There are more important things :pepeBuddha:', 'hell yeah', 'bro', 'bro...', 'kino', 'I love people like you', 
'No\n https://tenor.com/view/keanu-reeves-john-wick-awesome-gif-18042382', ':eye:', 'I love Molly Rankin', 'listen to song', ':situation:', ':liminal:', 'have you watched Succession yet',
'cringe', 'based', "I'm just so tired", "No I do not know when the next video is coming out", "Don't you have better things to do", ":catnod:", ":catnope:", ":awkward:"]
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

consumer_key = environ.get('CONSUMER_KEY')
consumer_secret = environ.get('CONSUMER_SECRET')
access_token = environ.get('ACCESS_TOKEN')
access_token_secret = environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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

def get_tweet():
    newest_tweet = 0
    channel = client.get_channel(972326727583948820)
    while True:
        tweets_list = api.user_timeline(user_id='Acerola_t', count=1)

        tweet = tweets_list[0]
        tweet_id = tweet.id
        if tweet_id != newest_tweet:
            newest_tweet = tweet_id
            if tweet.in_reply_to_screen_name == None and tweet.referenced_tweets == None:
                client.loop.create_task(channel.send("\thttps://twitter.com/Acerola_t/status/" + str(tweet.id)))

        time.sleep(30)

@client.event
async def on_ready():
    print('Logged in')
    x = threading.Thread(target=get_tweet, daemon=True)
    x.start()

@client.event
async def on_message(message):
    content = message.content.lower()
    user = str(message.author).split('#')[0]
    server = str(message.guild)
    id = message.author.id

    if message.author == client.user:
        return
    '''
    if user == "Acerola":
        await message.channel.send(id)
        fetched_user = await client.fetch_user(id)
        fetched_user = str(fetched_user).split('#')[0]
        await message.channel.send(fetched_user)
    '''
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
            stored_id = sorted_leaderboard[i][0]
            fetched_user = await client.fetch_user(stored_id)
            fetched_user = str(fetched_user).split('#')[0]

            leaderboard_string += f"#{i + 1} {fetched_user}: {sorted_leaderboard[i][1]}\n"
        leaderboard_string += f"\n```"

        await message.channel.send(leaderboard_string)
        return

    if 'bro' in content or 'vro' in content or 'bri' in content:
        bro_leaderboard[server][id] += 1
        with open('broboard.txt', 'w') as outfile:
            json.dump(bro_leaderboard, outfile)

    
client.run(TOKEN)
