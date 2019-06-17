import discord, asyncio, logging
from discord.ext import commands
import time, datetime
import sys

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)
battleOn = False
civs = {"Greeks":datetime.datetime.now(),"Egyptions":datetime.datetime.now(),"Samurai":datetime.datetime.now(),"Romans":datetime.datetime.now(),"Vikings":datetime.datetime.now(),"Persians":datetime.datetime.now()}

def setup(bot):
    bot.add_cog(raid(bot))

class raid(commands.Cog):
    """Raid cog!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def raid(self,ctx,defending: discord.Role=None):
        """RAiD a CIV"""
        global battleOn,civs
        if not battleOn:
            self.bot.get_channel(564225877785706516)
            attacking = None
            for role in ctx.author.roles:
                if role.name in civs.keys():
                    attacking = role
                    pass
            if attacking == None:
                return
            if defending == None or defending.name not in civs.keys():
                await ctx.send_help(ctx.command)
                return
            if defending == attacking:
                await ctx.send("You can't raid yourself!")
                return
            if civs[attacking.name] < datetime.datetime.now():
                pass
            else:
                timeleft = (civs[attacking.name] - datetime.datetime.now()).minute
                await ctx.send("Your civ needs to wait {} minutes until you can raid again!".format(timeleft))
            def check(m):
                return m.channel == ctx.channel and not m.author.bot
            usercooldown = {}
            endTime = datetime.datetime.now() + datetime.timedelta(minutes=10)
            damage = 0
            defence = 0
            await ctx.send("{} is now raiding {}!".format(attacking.mention,defending.mention))
            battleOn = True
            while datetime.datetime.now() < endTime:
                try:
                    msg = await self.bot.wait_for("message", check=check,timeout=5)
                except asyncio.TimeoutError:
                    pass
                else:
                    if msg.author.id not in usercooldown.keys():
                        usercooldown[msg.author.id] = datetime.datetime.now() - datetime.timedelta(seconds=1)
                    if attacking in msg.author.roles:
                        if msg.content == 'attack' or msg.content == 'Attack':
                            if datetime.datetime.now() > usercooldown[msg.author.id]:
                                damage += 50
                                await ctx.send("{} attacked! {} have done {} damage!".format(msg.author.display_name,attacking,damage))
                                usercooldown[msg.author.id] = datetime.datetime.now() + datetime.timedelta(seconds=45)
                            else:
                                timeleft = (usercooldown[msg.author.id] - datetime.datetime.now()).seconds
                                await ctx.send("You have to wait {} seconds before the next action.".format(timeleft))
                    elif defending in msg.author.roles:
                        if msg.content == 'defend' or msg.content == 'Defend':
                            if datetime.datetime.now() > usercooldown[msg.author.id]:
                                defence += 75
                                await ctx.send("{} defended! {} have got {} protection!".format(msg.author.display_name,defending,defence))
                                usercooldown[msg.author.id] = datetime.datetime.now() + datetime.timedelta(seconds=45)
                            else:
                                timeleft = (usercooldown[msg.author.id] - datetime.datetime.now()).seconds
                                await ctx.send("You have to wait {} seconds before the next action.".format(timeleft))
            message = await ctx.send("Time Over! Calculating Results")
            await asyncio.sleep(0.6)
            await message.edit(content="Time Over! Calculating Results.")
            await asyncio.sleep(0.2)
            await message.edit(content="Time Over! Calculating Results..")
            await asyncio.sleep(1)
            await message.edit(content="Time Over! Calculating Results...")
            await asyncio.sleep(2)
            result = (1000 + damage) - (1000 + defence)
            if result < 0: #DEFEND
                await ctx.send("{} Win by {} damage!".format(defending.mention,result))
            elif result > 1: #ATTACK
                await ctx.send("{} Win by {} damage!".format(attacking.mention,result))
            else:
                await ctx.send("Draw")
            civs[attacking.name] = datetime.datetime.now() + datetime.timedelta(hours=1)
        else:
            await ctx.send("There is already a raid going on somewhere, please wait until it ends")
