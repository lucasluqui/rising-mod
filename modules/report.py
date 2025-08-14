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

class report:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def report(self, ctx, heroName, evidence, *, reason):
        
        # Process the command if the player is linked and is not muted.
        if "player" in [y.name.lower() for y in ctx.message.author.roles] and not "muted" in [y.name.lower() for y in ctx.message.author.roles]:
            
            # Deletes original command message.
            await self.bot.delete_message(ctx.message)
            
            # Saves timestamp.
            vban_timestamp = datetime.datetime.now()
            
            # Tells the user the vote ban was successfully sent.
            await self.bot.say('Your report was successfully sent, <@{}>.'.format(str(ctx.message.author.id)))
            
            # Sends the vote ban to the channel.
            callout_channel = self.bot.get_channel(settings['votebans_channel'])
            report_embed = discord.Embed(title="Vote Ban!", description='Hello! Please watch the evidence below and vote on the suspect. Thanks!', colour=discord.Colour.red())
            report_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/384485467770454026.png")
            report_embed.add_field(name="Hero name (Suspect)", value=heroName, inline=False)
            report_embed.add_field(name="Evidence", value=evidence, inline=False)
            report_embed.add_field(name="Reason/Comment", value=reason, inline=False)
            report_embed.set_footer(text='A vote ban requested by: {}.'.format(str(ctx.message.author)))
            
            # Adds reactions to the vote ban message.
            reportembed_msg = await self.bot.send_message(callout_channel, embed=report_embed)
            await self.bot.add_reaction(reportembed_msg, '🔨')
            await self.bot.add_reaction(reportembed_msg, '🤦')

            # Time until vote ban ends. Default is 14400 seconds (5 hours).
            await asyncio.sleep(14400)
            
            # Logs the vote ban results and retreives date timestamp.
            message = await self.bot.get_message(callout_channel, reportembed_msg.id)
            hammer_reactions = message.reactions[0].count - 1
            facep_reactions = message.reactions[1].count - 1
            vban_date = vban_timestamp.date()
            vote_ban_log = self.bot.get_channel(settings['votebanslog_channel'])
            
            # Sends the vote ban results logging embed to the vote ban log channel.
            vbanlog_embed = discord.Embed(title="Vote Ban Log", description='Decide the fate of this player...', colour=0x5f8fcc)
            vbanlog_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/396521773652508684.png")
            vbanlog_embed.add_field(name="Hero name (Suspect)", value=heroName, inline=False)
            vbanlog_embed.add_field(name="Evidence provided", value=evidence, inline=False)
            vbanlog_embed.add_field(name="Reason/Comment", value=reason, inline=False)
            vbanlog_embed.add_field(name="Votes in favor", value='🔨 {}'.format(str(hammer_reactions)), inline=True)
            vbanlog_embed.add_field(name="Votes against", value='🤦 {}'.format(str(facep_reactions)), inline=True)
            vbanlog_embed.set_footer(text='A vote ban requested by: {}. Date: {}.'.format(str(ctx.message.author), str(vban_date)))
            await self.bot.send_message(vote_ban_log, embed=vbanlog_embed)
            
            # Edits the original vote ban message letting people know that the vote ban has ended, and removes existing reactions on it.
            report_embed_ended = discord.Embed(title="Vote Ban Ended!", description='Thanks everyone for submitting your votes!', colour=discord.Colour.orange())
            report_embed_ended.set_thumbnail(url="https://cdn.discordapp.com/emojis/384485467921317900.png")
            report_embed_ended.add_field(name="Reported player", value=heroName, inline=False)
            report_embed_ended.set_footer(text='A vote ban requested by: {}.'.format(str(ctx.message.author)))
            report_embed_ended_msg = await self.bot.edit_message(reportembed_msg, embed=report_embed_ended)
            await self.bot.clear_reactions(report_embed_ended_msg)
            
            # Sends an alert to review the ended vote ban using @here.
            alert_channel = self.bot.get_channel(settings['alerts_channel'])
            report_embed_ended_alert = discord.Embed(title="There's a vote ban to review...", description="Please review the latest ended vote ban in <#400422801250582548>.", colour=discord.Colour.orange())
            await self.bot.send_message(alert_channel, '@here')
            await self.bot.send_message(alert_channel, embed=report_embed_ended_alert)
        
        # If they're not linked, they won't be able to send vote bans.
        elif not "player" in [y.name.lower() for y in ctx.message.author.roles]:
           await self.bot.say("Sorry <@{}>, you need to link your Discord account in order to start a report.".format(str(ctx.message.author.id)))
        
        # If they're muted, they won't be able to send vote bans.
        elif "muted" in [y.name.lower() for y in ctx.message.author.roles]:
            await self.bot.say("Sorry <@{}>, you can't report while being muted.".format(str(ctx.message.author.id)))

def setup(bot):
    bot.add_cog(report(bot))