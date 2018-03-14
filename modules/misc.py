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

class misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self):
        
        # Load about file.
        aboutPath = "./about.json"
        with open(aboutPath) as f:
            about = json.load(f)
        
        # Sends the "about" embed.
        about_msg = discord.Embed(title="About", description="Useful information related to " + about['botname'] + ".", colour=discord.Colour.red())
        about_msg.add_field(name="Bot name", value=about['botname'])
        about_msg.add_field(name="Bot developer", value=about['botdev'])
        about_msg.add_field(name="Library used", value=about['botlibrary'])
        about_msg.add_field(name="Bot version", value=about['version'] + " released on " + about['versionday'] + ".")
        await self.bot.say(embed=about_msg)

    @commands.command(pass_context=True)
    async def modulelist(self, ctx):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Sends the module list.
            await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Modules", description='\n moduleMgn\n help\n chatFilter\n mute\n tempMute\n kick\n ban\n ping\n misc\n fun\n giveaway\n report\n bug\n suggestion\n mutedCheck\n helper\n errorHandler\n greeting', colour=discord.Colour.gold()))
        
        # If the user is not inside the team role.
        if "team" not in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say('You are not allowed to do this.')

    @commands.cooldown(rate=1, per=3600, type=commands.BucketType.user)
    @commands.command(pass_context=True, aliases=['registration'])
    async def registrations(self, ctx):
        
        # Sends the current status.
        status_tag = await self.bot.send_message(ctx.message.channel, '<@{}>,'.format(str(ctx.message.author.id)))
        status = await self.bot.send_message(ctx.message.channel, embed=discord.Embed(title="Registrations", description="Status: Open.", colour=discord.Colour.green()))
        
        # Deletes the command message.
        await self.bot.delete_message(ctx.message)
        
        # Waits 30 seconds and deletes the response with status.
        await asyncio.sleep (30)
        try:
            await self.bot.delete_message(status_tag)
            await self.bot.delete_message(status)
        except:
            pass

    @commands.command(pass_context=True)
    async def rename(self, ctx, *, newName):

        # Process the command if the user is in team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Rename the bot with the entered name.
            await self.bot.edit_profile(username=newName)

    @commands.command(pass_context=True)
    async def changelog(self, ctx):

        # Process the command if the user is in team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Load changelog.
            changelogPath = "./changelog.txt"
            changelog = open(changelogPath, "r") 
            
            # Send the changelog and close the file.
            await self.bot.send_message(ctx.message.channel, "```" + changelog.read() + "```")
            changelog.close()

def setup(bot):
    bot.add_cog(misc(bot))