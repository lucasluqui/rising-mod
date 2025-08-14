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

class fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def yo(self, ctx):
        
        # Process the command if the user in inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Deletes the message and salutes the user.
            await self.bot.delete_message(ctx.message)
            await self.bot.say('yo, <@{}>. 🤝'.format(str(ctx.message.author.id)))

    @commands.command(pass_context=True)
    async def say(self, ctx, *, message):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Deletes the command and sends the message.
            await self.bot.delete_message(ctx.message)
            await self.bot.say(message)

    @commands.command(pass_context=True, aliases=['8ball'])
    async def question(self, ctx, *, message):
        
        # Process the command if the user is inside the team role.
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Possible answers.
            answers = ["Yes", "No", "I don't know", "Probably", "😂", "🤔", "😤", "🤷🏻‍", "😳"]
            
            # Prints the asked question and an answer for it.
            answer_embed = discord.Embed(colour=0xef0bd8)
            answer_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/396521773132283914.png")
            answer_embed.add_field(name="Question", value=message, inline=False)
            answer_embed.add_field(name="Answer", value=random.choice(answers), inline=False)
            answer_embed.set_footer(text='At request of: {}.'.format(str(ctx.message.author)))
            await self.bot.send_message(ctx.message.channel, embed=answer_embed)
            
            # Deletes the original message.
            await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(fun(bot))