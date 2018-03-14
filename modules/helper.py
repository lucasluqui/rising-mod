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

# Load helpmessages.json
helpMessagesPath = 'modules/data/helpMessages.json'
with open(helpMessagesPath) as f:
    helpMessages = json.load(f)

class helper:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        for msg in helpMessages:
            
            # Process the event if there's a matching content in the message with the help messages, and the user isn't inside team role.
            if msg in message.content and not "team" in [y.name.lower() for y in message.author.roles]:
                
                # Tries to send a DM to the author of the trigger.
                try:
                    
                    # Deletes the trigger message and proceeds to send a DM.
                    await self.bot.delete_message(message)
                    await self.bot.send_message(message.author, "Please read the channel <#396340406603743233> to check backend and server conditions. Thanks.")
                
                # In case the author has DMs blocked, sends the message in the server.
                except:
                    
                    # Deletes the trigger message and proceeds to send a message to the user in the server.
                    await self.bot.send_message(message.channel, "<@{}>, please read the channel <#396340406603743233> to check backend and server conditions. Thanks.".format(message.author.id))
                    await self.bot.delete_message(message)

def setup(bot):
    bot.add_cog(helper(bot))