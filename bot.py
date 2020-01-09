import os
import wolframalpha
import discord
import re
import wikipedia
import requests
import io
import aiohttp
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WOLFRAM = os.getenv('WOLFRAMALPHA')
RAPIDAPI = os.getenv('RAPIDAPI')

wolfclient = wolframalpha.Client(app_id=WOLFRAM)
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

    if message.content.startswith('.img'):
        trim = re.compile(r"@|.img")
        q = re.sub(trim, '', message.content)
        pageNumber = 1
        pageSize = 10
        autoCorrect = True
        safeSearch = False

        response = requests.get(
            "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI?q={}&amp;pageNumber={}&amp;pageSize={}&amp;autocorrect={}&amp;safeSearch={}".format(
                q, pageNumber, pageSize, autoCorrect, safeSearch),
            headers={
                "X-RapidAPI-Key": RAPIDAPI,
                "X-RapidApi-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
            }
            ).json()

        print(response)
        for image in response["value"]:
            imageUrl = image["url"]
            async with aiohttp.ClientSession() as session:
                async with session.get(imageUrl) as resp:
                    if resp.status != 200:
                        return await message.channel.send('Couldnt download file')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(file=discord.File(data, 'image.png'))



    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)

