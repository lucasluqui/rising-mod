import asyncio
import copy
import datetime
import inspect
import random
import sys
import textwrap
import time
import random
import logging
import json
from collections import Counter, OrderedDict
import discord
from discord.ext import commands
from   discord import errors
import subprocess
import traceback

class ping:
    def __init__(self, bot):
        self.bot = bot

    # Limits use to 1 per minute.
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            t1 = ctx.message.timestamp
            m = await self.bot.say('...')
            
            # Gets the timestamp from the command message and the "m" message, and multiplies the difference by 1000. (ms)
            time = (m.timestamp-t1).total_seconds() * 1000
            
            # Sleeps for 1 second to lower the chances of a timestamp below 0 or no timestamp at all.
            await asyncio.sleep(1)
            
            # If the timestamp is between 1 and 150.
            if 1 <= time <= 150:
                await self.bot.say(embed=discord.Embed(title="Pong!", description="{}ms :thumbsup:".format(int(time)), colour=discord.Colour.green()))
                await self.bot.delete_message(m)
            
            # If the timestamp higher than 300.
            elif time > 300:
                await self.bot.say(embed=discord.Embed(title="Pong!", description="{}ms :thumbsdown:".format(int(time)), colour=discord.Colour.red()))
                await self.bot.delete_message(m)
            
            # If the timestamp is below 0. (rare bug, never found the cause)
            elif time <= 0:
                await self.bot.say(embed=discord.Embed(title="Pong?", description="{}ms :thinking:".format(int(time)), colour=0x000000))
                await self.bot.delete_message(m)
            
            # Tries to edit the "m" message incase the timestamp isn't received.
            try:
                await asyncio.sleep(3)
                await self.bot.edit_message(m, '`Discord API: Failed to ping bot.`')
            
            # If the timestamp was received, it returns.
            except:
                return
        
        # If the user is not inside the team role.
        elif not "team" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say('You are not allowed to ping the bot.')

def setup(bot):
    bot.add_cog(ping(bot))