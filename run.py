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
client = discord.Client()

# Load settings.
with open("settings.json") as f:
    settings = json.load(f)

# Setups logging type and format.
logging.basicConfig (
    level = logging.INFO,
    style = '{',
    datefmt = "%d/%m/%Y %H:%M:%S",
    format = "\n{asctime} [{levelname}] {name}:\n{message}"
)

# Bot prefix.
bot = commands.Bot(command_prefix=(settings['prefix']))

# Disable default help command from discord.py.
bot.remove_command('help')

@bot.event
async def on_ready():
    
    # Module list.

    modules = (
        "moduleHandler",
        "help",
        "mute",
        "tempMute",
        "kick",
        "ban",
        "ping",
        "misc",
        "fun",
        "giveaway",
        "report",
        "bug",
        "suggestion",
        "mutedCheck",
        "chatFilter",
        "errorHandler",
	"greeting"
    )

    # Load modules.
    for m in modules:
        bot.load_extension("modules.{}".format(m))
    
    # Changes game presence.
    await bot.change_presence(game=discord.Game(name=settings['status'], type=settings['rpctype']))
    
    # Prints startup to console.
    print("Started watch session as: ID {} ({}#{})".format(bot.user.id, bot.user.name, bot.user.discriminator))
    
    # Announces startup.
    announcement_channel = bot.get_channel(settings['announcement_channel'])
    await bot.send_message(announcement_channel, "Started watch session as: ID {} ({}#{})".format(bot.user.id, bot.user.name, bot.user.discriminator))

bot.run(settings['token'])
