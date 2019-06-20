import discord, asyncio, datetime, time, random, platform
from discord.ext import commands

def setup(bot):
    bot.add_cog(owner(bot))

class owner(commands.Cog):
    """Various things for the owner!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        """Shuts the bot down"""
        await ctx.send("👋 Goodbye")
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def run(self,ctx,*,command):
        """Runs a thing"""
        try:
            exec(command)
        except:
            return
        await ctx.message.add_reaction("✅")

    @commands.command(aliases = ['load'])
    @commands.is_owner()
    async def reload(self,ctx,cog):
        """Reloads a cog."""
        self.bot.reload_extension(cog)
        await ctx.send("Cog {} reloaded.".format(cog))

    @commands.command()
    async def uptime(self,ctx):
        """Shows you how long the bot has been online"""
        currentTime = time.time()
        uptime = int(round(currentTime - self.bot.startTime))
        uptime = str(datetime.timedelta(seconds=uptime))
        colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
        embed = discord.Embed(title="I have been up for", description=uptime, color=colour)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self,ctx):
        """Shows info about the bot"""
        colour = discord.Colour.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
        embed = discord.Embed(colour=colour,description="A bot made specifically for the HistoryWars discord!")
        embed.set_author(name="HistoryWarsBot", url="https://wwww.github.com/JdavisBro/historywarsbot", icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Creators:", value="JdavisBro#2640 (Raid)\nMrEdinLaw#1058 (Leaderboard)", inline=True)
        embed.add_field(name="Python Version:", value="[{}](https://www.python.org)".format(platform.python_version()), inline=True)
        embed.add_field(name="Discord.py Version:", value="[{}](https://github.com/Rapptz/discord.py)".format(discord.__version__), inline=True)
        await ctx.send(embed=embed)
