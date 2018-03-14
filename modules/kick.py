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

# Load settings.
settingsPath = "./settings.json"
with open(settingsPath) as f:
    settings = json.load(f)

class kick:
    def __init__(self, bot):
        self.bot = bot

    # Limits the use to 2 per hour.
    @commands.cooldown(rate=2, per=3600, type=commands.BucketType.user)
    @commands.command(pass_context=True)
    async def kick(self, ctx, member:discord.Member, *, reason):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Tries to message the kicked user via DM.
            try:
                await self.bot.send_message(member, "You have been kicked by **{}#{}**. Reason: `{}`\nYou can join the server again with another invite link.".format(str(ctx.message.author.name), str(ctx.message.author.discriminator), str(reason)))
            except:
                pass
            
            # Kicks the targeted user and announces it.
            await self.bot.kick(member)
            await self.bot.say("**<@{}>** was kicked successfully.".format(member.id))
            
            # Sends the kick log to admin alerts.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Kick", description='<@{}> has kicked <@{}>. Reason: `'.format(str(ctx.message.author.id), member.id) + reason + '`.', colour=0xf2801d))
        
        # If the command caller isn't inside the team role.
        elif not "team" in [y.name.lower() for y in message.author.roles]:
            await self.bot.say('You are not allowed to do this.')
        
        # If the user entered isn't found.
        else:
            await self.bot.say("User not found.")

def setup(bot):
    bot.add_cog(kick(bot))