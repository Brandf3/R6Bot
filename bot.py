import os
import discord
from dotenv import load_dotenv
import shlex
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

market = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        channel = message.channel
        await channel.send('Bot message!')
        
    elif message.content.startswith('!market'):
        channel = message.channel

        text = message.content
        textList = shlex.split(text)
        user = message.author

        if textList[1] == 'add':
            item = textList[2]
            price = textList[3]
            description = textList[4]

            s = str(user) + " is selling " + item + " for **" + price + "**. Description: " + description

            if item in market:
                market[item].append(s)
            else:
                market[item] = [s]
    
        if textList[1] == 'search':
            item = textList[2]

            if item in market:
                s = ""
                listings = market[item]
                for x in listings:
                    s += x + "\n"
                await channel.send(s)
                    
            else:
                await channel.send("Sorry, there are no listings for " + item + ".")

    elif message.content.startswith('!ops'):
        pass
    elif message.content.startswith('!stats'):
        #some setup Stuff
        channel = message.channel
        text = message.content
        textList = shlex.split(text)
        user = textList[1]

        # get stats
        r = requests.get('https://r6.tracker.network/profile/pc/' + user)
        stats = r.text
        # get WinLoss
        index1 = stats.find('PVPWLRatio')
        index1 += 13
        index2 = stats.find('<', index1) - 1
        winLoss = stats[index1:index2]
        # Get KD
        index1 = stats.find('PVPKDRatio')
        index1 += 13
        index2 = stats.find('<', index1) - 1
        killDeath = stats[index1:index2]
        # Get headshot Percent
        index1 = stats.find('PVPAccuracy')
        index1 += 14
        index2 = stats.find('<', index1) - 1
        headShotPercent = stats[index1:index2]
        s = user + ":" + \
                   "\n    WL: " + winLoss + \
                   "\n    KD: " + killDeath + \
                   "\n    HeadShots: "  + headShotPercent
        await channel.send(s)
    elif message.content.startswith('!mmr'):
        pass
    elif message.content.startswith('!wins'):
        channel = message.channel

        text = message.content
        textList = shlex.split(text)
        user = textList[1]

        r = requests.get('https://r6.tracker.network/profile/pc/' + user)
        stats = r.text
        index = stats.find('PVPMatchesWon')
        index += 16
        index2 = index + stats[index:].find('<') - 1
        wins = stats[index:index2]
        s = user + " has " + wins + " wins."
        await channel.send(s)

client.run(TOKEN)
