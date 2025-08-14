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

class giveaway:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def giveaway(self, ctx, channelId, duration, *, prize):
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            totalDuration = int(duration)*3600
            targetChannel = self.bot.get_channel(channelId)
            giveaway_embed = discord.Embed(title="Giveaway", description="Welcome to the giveaway,\nreact with the 🎉 reaction for an entry on the giveaway.", colour=0xef0bd8)
            giveaway_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/396514815855558679.png")
            giveaway_embed.add_field(name="Prize", value=prize, inline=True)
            giveaway_embed.add_field(name="Duration", value="{} hours.".format(duration), inline=True)
            giveaway_embed.set_footer(text='At request of: {}.'.format(str(ctx.message.author)))
            giveawaymsg = await self.bot.send_message(targetChannel, embed=giveaway_embed)
            await self.bot.add_reaction(giveawaymsg, '🎉')
            
            # Task sleeps until giveaway ends.
            await asyncio.sleep(totalDuration)
            
            # Grabs a random user.
            giveawaymsg = await self.bot.get_message(targetChannel, giveawaymsg.id)
            reaction = discord.utils.get(giveawaymsg.reactions, emoji='🎉')
            users = await self.bot.get_reaction_users(reaction)
            random_user = random.choice(users)

            # Grabs the total participants count.
            participants = giveawaymsg.reactions[0].count - 1
            
            # Creates the winner announcement and clears the giveaway reactions.
            giveawayended_embed = discord.Embed(title="Giveaway Ended", description="Congratulations <@{}>, you just won the giveaway!".format(random_user.id), colour=0xef0bd8)
            giveawayended_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/397150027748868096.png")
            giveawayended_embed.add_field(name="Prize", value=prize, inline=True)
            giveawayended_embed.add_field(name="Total participants", value='👤 {}'.format(str(participants), inline=True))
            giveawayended_embed.add_field(name="Winner", value='<@{}>'.format(random_user.id), inline=True)
            giveawayended_embed.set_footer(text='At request of: {}.'.format(str(ctx.message.author)))
            await self.bot.clear_reactions(giveawaymsg)

            # Sends the winner announcement.
            await self.bot.edit_message(giveawaymsg, embed=giveawayended_embed)
            await self.bot.send_message(targetChannel, '💎 Congratulations **{}**, you just won the giveaway!'.format(str(random_user.display_name)))

    @commands.command(pass_context=True)
    async def fastgiveaway(self, ctx, duration, *, prize):
        if "team" in [y.name.lower() for y in ctx.message.author.roles]:
            totalDuration = int(duration)
            giveaway_embed = discord.Embed(title="Giveaway", description="Welcome to the giveaway,\nreact with the 🎉 reaction for an entry on the giveaway.", colour=0xef0bd8)
            giveaway_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/396514815855558679.png")
            giveaway_embed.add_field(name="Prize", value=prize, inline=True)
            giveaway_embed.add_field(name="Duration", value="{} seconds.".format(duration), inline=True)
            giveaway_embed.set_footer(text='At request of: {}.'.format(str(ctx.message.author)))
            giveawaymsg = await self.bot.send_message(ctx.message.channel, embed=giveaway_embed)
            await self.bot.add_reaction(giveawaymsg, '🎉')
            
            # Task sleeps until giveaway ends.
            await asyncio.sleep(totalDuration)
            
            # Grabs a random user.
            giveawaymsg = await self.bot.get_message(ctx.message.channel, giveawaymsg.id)
            reaction = discord.utils.get(giveawaymsg.reactions, emoji='🎉')
            users = await self.bot.get_reaction_users(reaction)
            random_user = random.choice(users)

            # Grabs the total participants count.
            participants = giveawaymsg.reactions[0].count - 1
            
            # Creates the winner announcement and clears the giveaway reactions.
            giveawayended_embed = discord.Embed(title="Giveaway Ended", description="Congratulations <@{}>, you just won the giveaway!".format(random_user.id), colour=0xef0bd8)
            giveawayended_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/397150027748868096.png")
            giveawayended_embed.add_field(name="Prize", value=prize, inline=True)
            giveawayended_embed.add_field(name="Total participants", value='👤 {}'.format(str(participants), inline=True))
            giveawayended_embed.add_field(name="Winner", value='<@{}>'.format(random_user.id), inline=True)
            giveawayended_embed.set_footer(text='At request of: {}.'.format(str(ctx.message.author)))
            await self.bot.clear_reactions(giveawaymsg)

            # Sends the winner announcement.
            await self.bot.edit_message(giveawaymsg, embed=giveawayended_embed)
            await self.bot.send_message(ctx.message.channel, '💎 Congratulations **{}**, you just won the giveaway!'.format(str(random_user.display_name)))


def setup(bot):
    bot.add_cog(giveaway(bot))