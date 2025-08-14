import asyncio
import copy
import datetime
import sys
import time
import logging
import json
from collections import Counter, OrderedDict
import discord
from discord.ext import commands
from   discord import errors

# Load settings.
settingsPath = "./settings.json"
with open(settingsPath) as f:
    settings = json.load(f)

# Loads shitpostfilter.json
shitpostFilterPath = 'modules/data/shitpostFilter.json'
with open(shitpostFilterPath) as f:
    shitpostFilter = json.load(f)

# Loads dilfilter.json
dilFilterPath = 'modules/data/dilFilter.json'
with open(dilFilterPath) as f:
    dilFilter = json.load(f)

class chatFilter:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        for msg in shitpostFilter:
            
            # Process the event if there's a matching content in the message with the shitpost filter, and the user isn't inside team role.
            if msg in message.content and not "team" in [y.name.lower() for y in message.author.roles]:
                
                # Sends the trigger to the chat filter channel.
                shitpost_feed = self.bot.get_channel(settings['filter_channel'])
                shitpost_embed = discord.Embed(title="Shitpost Filter", description='`{}`'.format(message.content), colour=discord.Colour.gold())
                shitpost_embed.set_footer(text='Sent by: {}. In channel: #{}.'.format(message.author, message.channel.name))
                await self.bot.send_message(shitpost_feed, embed=shitpost_embed)
                
                # Deletes the message.
                await self.bot.delete_message(message)
        
        for msg in dilFilter:
            
            # Process the event if there's a matching content in the message with the Discord Invite Link (DIL) filter, and the user isn't inside team role.
            if msg in message.content and not "team" in [y.name.lower() for y in message.author.roles]:
                
                # Sends the trigger to the chat filter channel.
                dil_feed = self.bot.get_channel(settings['filter_channel'])
                dil_embed = discord.Embed(title="DIL Filter", description='`{}`'.format(message.content), colour=0x7289DA)
                dil_embed.set_footer(text='Sent by: {}. In channel: #{}.'.format(message.author, message.channel.name))
                await self.bot.send_message(dil_feed, embed=dil_embed)
                
                # Deletes the message.
                await self.bot.delete_message(message)

def setup(bot):
    bot.add_cog(chatFilter(bot))