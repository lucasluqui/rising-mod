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

class ban:
    def __init__(self, bot):
        self.bot = bot

    # Limits command to 1 use per hour.  
    @commands.cooldown(rate=1, per=3600, type=commands.BucketType.user)
    @commands.command(pass_context=True)
    async def ban(self, ctx, member:discord.Member, *, reason):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Tries to message the banned user via DM.
            try:
                await self.bot.send_message(member, "You have been banned by **{}#{}**. Reason: `{}`".format(str(ctx.message.author.name), str(ctx.message.author.discriminator), str(reason)))
            except:
                pass

            # Bans the user and announces it.
            await self.bot.ban(member)
            await self.bot.say("**<@{}>** was successfully banned.".format(member.id))
            
            # Sends the ban info to admin alerts.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Ban", description='<@{}> has banned <@{}>. Reason: `'.format(str(ctx.message.author.id), member.id) + reason + '`.', colour=0xf40e0e))
        
        # If user isn't in the team, he wont be able to run the command.
        elif not "team" in [y.name.lower() for y in message.author.roles]:
            await self.bot.say('You are not allowed to do this.')
        
        # If the user entered isn't found.
        else:
            await self.bot.say("User not found.")

    @commands.command(pass_context=True)
    async def unban(self, ctx, userId):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Gets the user by ID, and announces the unban.
            getuser = await self.bot.get_user_info(userId)
            await self.bot.unban(ctx.message.server, getuser)
            await self.bot.say("**<@{}>** was successfully unbanned.".format(userId))
            
            # Sends the unban info to admin alerts.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Unban", description='<@{}> has unbanned <@{}>.'.format(str(ctx.message.author.id), userId), colour=discord.Colour.green()))
        
        # If user isn't in the team, he wont be able to run the command.
        elif not "team" in [y.name.lower() for y in message.author.roles]:
            await self.bot.say('You are not allowed to do this.')
        
        # If the user entered isn't found.
        else:
            await self.bot.say("User not found.")

    @commands.command(pass_context=True)
    async def banlist(self, ctx):

        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
 
            # Gets the banned list.
            banlist = await self.bot.get_bans(ctx.message.server)

            # Formats the list to Name, Discriminator and ID.
            banlistcount = int(len(banlist))
            banlistfmt = []
            for u in banlist:
                banlistfmt.append('{0.name}#{0.discriminator} (ID: {0.id})'.format(u))

            # Sends the message with the ban list.
            await self.bot.send_message(ctx.message.channel, "The following users are banned:\n ```" + '\n'.join(banlistfmt) + "```\n Total banned users: " + str(banlistcount))
            

def setup(bot):
    bot.add_cog(ban(bot))