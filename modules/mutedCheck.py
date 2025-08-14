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

# Information of the muted role.
Muted = discord.Role(id=settings['muted'],server=settings['server'])

class mutedCheck:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_member_join(self, member):
        
        # Load mutedUsers.txt
        with open('modules/data/mutedUsers.txt', 'r') as in_file:
            mutedUsers = in_file.readlines()

        # Checks if the joined member is inside the muted check.
        for id in mutedUsers:
            if member.id == id.strip():
                
                # If he is, it adds him back to the Muted role.
                await self.bot.add_roles(member, Muted)
                callout_channel = self.bot.get_channel(settings['alerts_channel'])
                await self.bot.send_message(callout_channel, embed=discord.Embed(title="Failed mute evade attempt", description="<@{}> tried to evade his mute... but failed :(".format(member.id), colour=0x404142))

    @commands.group(pass_context=True)
    async def mutecheck(self, ctx):
    
        # If there's no specific type of mute check requested.
        if ctx.invoked_subcommand is None:

            await self.bot.say('Correct usage: `~mutecheck add/remove @mention`')


    @mutecheck.command(pass_context=True, name="add")
    async def _add(self, ctx, member:discord.Member):
        
        # Process command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles] and "muted" in [y.name.lower() for y in member.roles]:
            
            # Adds mute check.
            with open('modules/data/mutedUsers.txt', 'a') as out_file:
                out_file.write('\n' + member.id)
            await self.bot.say("Successfully added a mute check to **<@{}>**.".format(member.id))
            
            out_file.close()
            
            # Sends the mute check log to the admin alerts channel.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Mute check", description='<@{}> has added a muted check to <@{}>.'.format(str(ctx.message.author.id), member.id), colour=0x2a2b2b))
        
        # If the targeted user is not muted.
        elif not "muted" in [y.name.lower() for y in member.roles]:
            await self.bot.say('This user is not muted.')
        
        # No permission.
        elif not "team" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("You are not allowed to do this.")

    @mutecheck.command(pass_context=True, name="remove")
    async def _remove(self, ctx, member:discord.Member):
        
        # Process command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Removes mute check.
            f = open("modules/data/mutedUsers.txt","r+")
            ids = f.readlines()
            f.seek(0)
            for id in ids:
                if id != member.id:
                    f.write(id)
            f.truncate()
            f.close()
            await self.bot.say("Successfully removed a mute check from **<@{}>**.".format(member.id))
            
            out_file.close()
            
            # Sends the mute check log to the admin alerts channel.
            callout_channel = self.bot.get_channel(settings['alerts_channel'])
            await self.bot.send_message(callout_channel, embed=discord.Embed(title="Mute check", description='<@{}> has added a muted check to <@{}>.'.format(str(ctx.message.author.id), member.id), colour=0x2a2b2b))
        
        # No permission.
        elif not "team" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("You are not allowed to do this.")

def setup(bot):
    bot.add_cog(mutedCheck(bot))