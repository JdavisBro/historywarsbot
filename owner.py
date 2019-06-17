import discord, asyncio
from discord.ext import commands

def setup(bot):
    bot.add_cog(owner(bot))

class owner(commands.Cog):
    """owner cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        await ctx.send("👋 Goodbye")
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def run(self,ctx,*,command):
        try:
            exec(command)
        except:
            return
        await ctx.message.add_reaction("✅")

    @commands.command(aliases = ['load'])
    @commands.is_owner()
    async def reload(self,ctx,cog):
        """Reloads a cog."""
        try:
            self.bot.reload_extension(cog)
        except:
            await ctx.send("Failed.")
            raise
        else:
            await ctx.send("Cog {} reloaded.".format(cog))