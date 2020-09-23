import os
import discord
from dotenv import load_dotenv
import shlex
import requests
from bs4 import BeautifulSoup


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    channel = message.channel
    text = message.content
    textList = shlex.split(text)
    user = textList[1]
    
    if message.content.startswith('!ops'):
        await ops(channel, user)
    elif message.content.startswith('!stats'):
        await stats(channel, user)
    elif message.content.startswith('!mmr'):
        pass
    elif message.content.startswith('!wins'):
        await wins(channel, user)


async def ops(channel, user):
    r = requests.get('https://r6.tracker.network/profile/pc/' + user + '/operators')
    if isValidPage(r):
        text = r.text
        soup = BeautifulSoup(text, features="html.parser")
        attackers = soup.find_all('table', { 'id' : 'operators-Attackers' })[0].find_all('span')
        defenders = soup.find_all('table', { 'id' : 'operators-Defenders' })[0].find_all('span')

        s = 'Top 3 attackers: ' + attackers[0].text.title() + ', ' + attackers[2].text.title() + ', ' + attackers[4].text.title() + \
                '\nTop 3 defenders: ' + defenders[0].text.title() + ', ' + defenders[2].text.title() + ', ' + defenders[4].text.title()
    else:
        s = 'Sorry, user stats not found.'
    await channel.send(s)


async def stats(channel, user):
    # get stats
    r = requests.get('https://r6.tracker.network/profile/pc/' + user)
    if isValidPage(r):
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
    else:
        s = 'Sorry, user stats not found.'
    await channel.send(s)


async def wins(channel, user):
    r = requests.get('https://r6.tracker.network/profile/pc/' + user)
    if isValidPage(r):
        stats = r.text
        index = stats.find('PVPMatchesWon')
        index += 16
        index2 = index + stats[index:].find('<') - 1
        wins = stats[index:index2]
        s = user + " has " + wins + " wins."
    else:
        s = 'Sorry, user stats not found.'
    await channel.send(s)


def isValidPage(r):
    if r.status_code == 404:
        return False
    return True
    #TODO make sure page isn't a 404


client.run(TOKEN)
