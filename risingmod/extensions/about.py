from discord.ext import commands
import discord


class About(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        return  # do something

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    @commands.command(aliases=['risingmod'])
    async def about(self, ctx):
        await ctx.send('test')


def setup(bot):
    bot.add_cog(About(bot))
