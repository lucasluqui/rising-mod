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

class helpp:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def help(self, ctx):

        # If there's no specific type of help requested.
        if ctx.invoked_subcommand is None:
            
            # Sends the help embed.
            help_embed = discord.Embed(title="Help", description="List of available commands.", colour=discord.Colour.green())
            help_embed.add_field(name="~report <hero name> <video evidence> <reason/comments>", value="Reports an user. You **need** to provide valid evidence and a reason/comment.", inline=False)
            help_embed.add_field(name="~bug <message>", value="Sends a bug report.", inline=False)
            help_embed.add_field(name="~suggestion <message>", value="Sends a suggestion.", inline=False)
            help_embed.add_field(name="~registrations", value="Checks registrations status for Rising Hub (limited to 1 per hour).", inline=False)
            await self.bot.say(embed=help_embed)

    @help.command(pass_context=True, name="staff")
    async def _staff(self, ctx):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            staffhelp_embed = discord.Embed(title="Staff commands", description="List of available staff commands.", colour=discord.Colour.gold())
            staffhelp_embed.add_field(name="~tempmute @mention <time in minutes> <reason>", value="Temporarily mutes targeted user.", inline=False)
            staffhelp_embed.add_field(name="~mute @mention <reason>", value="Mutes targeted user.", inline=False)
            staffhelp_embed.add_field(name="~mutecheck add @mention", value="Adds a mute check to target user. Prevents user from mute evading.", inline=False)
            staffhelp_embed.add_field(name="~mutecheck remove @mention", value="Removes a mute check from target user.", inline=False)
            staffhelp_embed.add_field(name="~unmute @mention", value="Unmutes targeted user.", inline=False)
            staffhelp_embed.add_field(name="~kick @mention <reason>", value="Kicks targeted user (limited to 2 per hour).", inline=False)
            staffhelp_embed.add_field(name="~ban @mention <reason>", value="Bans targeted user (limited to 1 per hour).", inline=False)
            staffhelp_embed.add_field(name="~banlist", value="Retrieves banned users list.", inline=False)
            staffhelp_embed.add_field(name="~unban <id>", value="Unbans targeted user.", inline=False)
            staffhelp_embed.add_field(name="~ping", value="Pings the bot. Returns latency in ms.", inline=False)
            staffhelp_embed.add_field(name="~yo", value="Bot salutes you.", inline=False)
            staffhelp_embed.add_field(name="~say <message>", value="Impersonate the bot with a message.", inline=False)
            staffhelp_embed.add_field(name="~question <question>", value="Bot answers your question.", inline=False)
            staffhelp_embed.add_field(name="~giveaway <channel id> <duration in hours> <prize>", value="Sends a giveaway to the target channel.", inline=False)
            staffhelp_embed.add_field(name="~fastgiveaway <duration in seconds> <prize>", value="Sends a fast giveaway to the current channel you're in.", inline=False)
            await self.bot.say(embed=staffhelp_embed)

        # If the user isn't inside the team role.
        elif "team" not in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("You are not part of the team.")

def setup(bot):
    bot.add_cog(helpp(bot))