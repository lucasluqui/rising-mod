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

class greeting:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_member_join(self, member):

        try:
            await self.bot.send_message(member, settings['welcome_message'])
        except:
            pass    

def setup(bot):
    bot.add_cog(greeting(bot))