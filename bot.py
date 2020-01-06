import os
import wolframalpha
import discord
import re
import wikipedia
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

wolfclient = wolframalpha.Client(app_id='X48LAH-RWEV576443')
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.content.startswith('jamie'):
        trim = re.compile(r"@|jamie")
        trimmed_str = re.sub(trim, '', message.content)
        def changeChar(word): #used to format query for API URL, WIP
            for letter in word:
                if letter != " ":
                    word = word.replace(letter, "%+")
                    return word
        changeChar(trimmed_str)
        url = 'http://api.wolframalpha.com/v1/simple?appid=X48LAH-RWEV576443&i='
        final_str = ''.join((url, trimmed_str))
        res = wolfclient.query(final_str)
        #if res['@success'] == 'false':
            #await message.channel.send('Could not resolve the question.')
        #else:
        await message.channel.send(res)

    if message.content.startswith('.wiki'):
            trim = re.compile(r"@|.wiki")
            trimmed_str = re.sub(trim, '', message.content)
            res = wikipedia.summary(trimmed_str, sentences=5, auto_suggest=True)
            await message.channel.send(res)

    #implement audio playback WIP
    if message.content.startswith('.play'):
            trim = re.compile(r"@|.play")
            trimmed_str = re.sub(trim, '', message.content)

    if message.content.startswith('hello'):
            await message.channel.send('Hello!')

client.run(TOKEN)

