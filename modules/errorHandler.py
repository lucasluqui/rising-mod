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

class errorHandler:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_command_error(self, error, ctx):
        
        if "muted" in [y.name.lower() for y in ctx.message.author.roles] or "player" not in [y.name.lower() for y in ctx.message.author.roles]:
            return
        
        # If the command doesn't exist.
        if isinstance(error, commands.CommandNotFound):
            await self.bot.send_message(ctx.message.channel, "`That command does not exist.`")
       
       
        # If the command is during a cooldown period.
        if isinstance(error, commands.CommandOnCooldown):
            await self.bot.send_message(ctx.message.channel, "`Command currently on cooldown.`")
        
        
        # If the user entered an invalid argument for a command.
        if isinstance(error, commands.BadArgument):
            await self.bot.send_message(ctx.message.channel, "`One of the arguments you entered wasn't correct.`")
        
        
        # If the command gets an error on invoke.
        if isinstance(error, commands.CommandInvokeError):
            await self.bot.send_message(ctx.message.channel, "`There was an unexpected error while invoking this command.`")

def setup(bot):
    bot.add_cog(errorHandler(bot))