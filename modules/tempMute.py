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

# Information for the muted role.
Muted = discord.Role(id=settings['muted'],server=settings['server'])

class tempMute:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def tempmute(self, ctx, member:discord.Member, mutedTime, *, reason):
        
        # Multiplies the received muted time by 60 and converts it into an integer.
        totalMutedTime = int(mutedTime)*60
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles] and totalMutedTime <= 86400 and not "muted" in [y.name.lower() for y in member.roles] and member.id != settings['botid']:
            
            # Adds the Muted role to the targeted user.
            await self.bot.add_roles(member, Muted)
            
            # Adds mute check.
            with open('modules/data/mutedUsers.txt', 'a') as out_file:
                out_file.write('\n' + member.id)
            out_file.close()
            
            # Announces mute.
            await self.bot.say("**<@{}>** was muted for **{}** minutes successfully.".format(member.id, mutedTime))

            # Tries to message to the temp muted user via DM.
            try:
                await self.bot.send_message(member, "You have been temporarily muted by **{}#{}** for **{}** minutes. Reason: `{}`".format(str(ctx.message.author.name), str(ctx.message.author.discriminator), mutedTime, str(reason)))
            except:
                pass
            
            # Logs the start of the temp mute to the admin alerts channel.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Temp mute", description='<@{}> has muted <@{}> {} minutes. Reason: `'.format(str(ctx.message.author.id), member.id, mutedTime) + reason + '`.', colour=discord.Colour.red()))
            
            # Task sleeps for the total temp mute time.
            await asyncio.sleep(totalMutedTime)
            
            # Task wakes up and removes the Muted role from the targeted user.
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
            
            # Tries to message to the finished temp muted user via DM.
            try:
                await self.bot.send_message(member, "Your temporary mute has ended. Please watch your behaviour from now on so you don't get muted again.")
            except:
                pass
            
            # Logs the end of the temp mute to the admin alerts channel.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Temp mute completed", description='<@{}> has completed his temp mute time.'.format(member.id), colour=discord.Colour.green()))
        
        # If the user to mute is the bot.
        elif member.id == settings['botid']:
            await self.bot.say("I can't mute myself.")
        
        # If the user is already muted.
        elif "muted" in [y.name.lower() for y in member.roles]:
            await self.bot.say('This user is already muted.')
        
        # Other situations.
        else:
            await self.bot.say("You are not allowed to do this or something went wrong.")

def setup(bot):
    bot.add_cog(tempMute(bot))