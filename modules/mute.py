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

# Muted role information.
Muted = discord.Role(id=settings['muted'],server=settings['server'])

class mute:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mute(self, ctx, member:discord.Member, *, reason):
        
        # Process command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles] and not "muted" in [y.name.lower() for y in member.roles] and member.id != settings['botid']:
            
            # Adds muted role to targeted user.
            await self.bot.add_roles(member, Muted)
            
            # Adds mute check.
            with open('modules/data/mutedUsers.txt', 'a') as out_file:
                out_file.write('\n' + member.id)
            out_file.close()
            
            # Announces mute.
            await self.bot.say("**<@{}>** was muted successfully.".format(member.id))

            # Tries to message to the muted user via DM.
            try:
                await self.bot.send_message(member, "You have been muted by **{}#{}**. Reason: `{}`".format(str(ctx.message.author.name), str(ctx.message.author.discriminator), str(reason)))
            except:
                pass
            
            # Sends the mute log to the admin alerts channel.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Mute", description='<@{}> has muted <@{}>. Reason: `'.format(str(ctx.message.author.id), member.id) + reason + '`.', colour=discord.Colour.red()))
        
        # If the user to mute is the bot.
        elif member.id == settings['botid']:
            await self.bot.say("I can't mute myself.")
        
        # If the targeted user is already muted.
        elif "muted" in [y.name.lower() for y in member.roles]:
            await self.bot.say('This user is already muted.')
        
        # No permission.
        elif not "team" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("You are not allowed to do this.")
    
    @commands.command(pass_context=True)
    async def unmute(self, ctx, member:discord.Member):
        
        # Process command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles] and "muted" in [y.name.lower() for y in member.roles]:
            
            # Removes muted role in the targeted user.
            await self.bot.remove_roles(member, Muted)

            # Removes mute check.
            f = open("modules/data/mutedUsers.txt","r+")
            ids = f.readlines()
            f.seek(0)
            for id in ids:
                if id != member.id:
                    f.write(id)
            f.truncate()
            f.close()

            await self.bot.say("**<@{}>** was unmuted successfully.".format(member.id))

            # Tries to message to the unmuted user via DM.
            try:
                await self.bot.send_message(member, "You have been unmuted by **{}#{}**. Please watch your behaviour from now on so you don't get muted again.".format(str(ctx.message.author.name), str(ctx.message.author.discriminator)))
            except:
                pass
            
            # Sends the unmute log to the admin alerts channel.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Unmute", description='<@{}> has unmuted <@{}>.'.format(str(ctx.message.author.id), member.id), colour=discord.Colour.green()))
        
        # If the targeted user is not muted.
        elif not "muted" in [y.name.lower() for y in member.roles]:
            await self.bot.say('This user is not muted.')
        
        # No permission.
        elif not "team" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("You are not allowed to do this.")

def setup(bot):
    bot.add_cog(mute(bot))