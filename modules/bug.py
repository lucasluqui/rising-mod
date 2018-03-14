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

class bug:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def bug(self, ctx, *, message):
        
        # Process the command if the user is linked and is not muted.
        if "player" in [y.name.lower() for y in ctx.message.author.roles] and not "muted" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Deletes the command message.
            await self.bot.delete_message(ctx.message)
            
            # Sends the reported bug to the bug reports channel.
            bug_channel = self.bot.get_channel(settings['bugs_channel'])
            bug_report_alert = discord.Embed(title="BUG REPORT", description=message, colour=discord.Colour.dark_teal())
            bug_report_alert.set_footer(text='Bug report sent by: {}.'.format(str(ctx.message.author)))
            await self.bot.send_message(bug_channel, embed=bug_report_alert)
            
            # Tells the user that his bug report has been sent successfully.
            await self.bot.say('Your bug report was sent successfully, <@{}>.'.format(str(ctx.message.author.id)))
        
        # If the user is not linked, the command won't run.
        elif not "player" in [y.name.lower() for y in ctx.message.author.roles]:
           await self.bot.say("Sorry <@{}>, you need to link your discord account in order to report a bug.".format(str(ctx.message.author.id)))
        
        # If the user is muted, the command won't run.
        elif "muted" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("Sorry <@{}>, you can't report a bug while being muted.".format(str(ctx.message.author.id)))

def setup(bot):
    bot.add_cog(bug(bot))