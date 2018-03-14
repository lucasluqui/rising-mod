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

class suggestion:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def suggestion(self, ctx, *, message):
        
        # Process the command if the user is linked and it isn't muted.
        if "player" in [y.name.lower() for y in ctx.message.author.roles] and not "muted" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Deletes the message.
            await self.bot.delete_message(ctx.message)
            
            # Sends the suggestion to the player suggestions channel.
            suggestion_channel = self.bot.get_channel(settings['suggestions_channel'])
            suggestion_alert = discord.Embed(title="SUGGESTION", description=message, colour=discord.Colour.magenta())
            suggestion_alert.set_footer(text='Suggestion sent by: {}.'.format(str(ctx.message.author)))
            suggestion_received = await self.bot.send_message(suggestion_channel, embed=suggestion_alert)
            
            # Adds reactions to the suggestion message.
            await self.bot.add_reaction(suggestion_received, '👍')
            await self.bot.add_reaction(suggestion_received, '👎')
            
            # Announces to the user that his reaction was received.
            await self.bot.say('Your suggestion was sent successfully, <@{}>.'.format(str(ctx.message.author.id)))
        
        # If the user is not linked.
        elif not "player" in [y.name.lower() for y in ctx.message.author.roles]:
           await self.bot.say("Sorry <@{}>, you need to link your discord account in order to send a suggestion.".format(str(ctx.message.author.id)))
        
        # If the user is muted.
        elif "muted" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("Sorry <@{}>, you can't send a suggestion while being muted.".format(str(ctx.message.author.id)))

def setup(bot):
    bot.add_cog(suggestion(bot))