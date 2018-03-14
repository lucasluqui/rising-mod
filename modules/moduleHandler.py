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

class moduleMgn:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def load(self, ctx, module):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Loads the extension and adds a check mark to the message.
            self.bot.load_extension("modules.{}".format(module))
            await self.bot.add_reaction(ctx.message, '✅')
        
        # If the command fails it adds a red cross to the message.
        else:
            await self.bot.add_reaction(ctx.message, '❌')

    @commands.command(pass_context=True)
    async def unload(self, ctx, module):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Unloads the extension and adds a check mark to the message.
            self.bot.unload_extension("modules.{}".format(module))
            await self.bot.add_reaction(ctx.message, '✅')
        
        # If the command fails, it adds a red cross to the message.
        else:
            await self.bot.add_reaction(ctx.message, '❌')

    @commands.command(pass_context=True)
    async def reload(self, ctx, module):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Reloads the extension and adds a check mark to the message.
            self.bot.unload_extension("modules.{}".format(module))
            await asyncio.sleep(3)
            self.bot.load_extension("modules.{}".format(module))
            await self.bot.add_reaction(ctx.message, '✅')
        
        # If the command fails, it adds a red cross to the message.
        else:
            await self.bot.add_reaction(ctx.message, '❌')

def setup(bot):
    bot.add_cog(moduleMgn(bot))