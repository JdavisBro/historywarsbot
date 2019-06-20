import discord
from discord.ext import commands
import sqlite3
import datetime

sql_config = sqlite3.connect('data.db')
sql_con = sql_config.cursor()
factions = ['viking', 'persian', 'roman', 'egyptian', 'greek', 'samurai']
items = ['coins', 'viking_loot', 'persian_loot', 'roman_loot', 'egyptian_loot', 'greek_loot', 'samurai_loot', 'weapons']

def setup(bot):
    bot.add_cog(leaderboard(bot))

class leaderboard(commands.Cog):
    """Made by: MrEdinLaw!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(506413971423625226, 506899380289142785, 548668450763964428)
    async def leaderboardhelp(self,ctx):
        await ctx.send(
            "Available Leaderboard Commands:\n\t+addweapon [faction] [weapon]\n\t+removeweapon [faction] [weapon]\n\t+sendstats [channel]\n\t+add [item] [faction] [amount]\n\t+resetData (Resets All Data)")


    @commands.command()
    @commands.has_any_role(506413971423625226, 506899380289142785, 548668450763964428)
    async def removeweapon(self,ctx, faction: str, *, weapon: str):
        faction = faction.lower()
        if faction.lower() in factions:
            try:
                sql_con.execute(f"SELECT `weapons` FROM `data` WHERE name = '{faction}'")
                weapons = sql_con.fetchone()[0].split(",")
            except:
                weapons = []

            if weapon in weapons:
                weapons.remove(weapon)
                weaponString = ",".join(weapons)
                sql_con.execute(f"UPDATE 'data' SET 'weapons' = '{weaponString}' WHERE name = '{faction}'")
                sql_config.commit()
                await ctx.send(f"Weapon **{weapon}** removed for **{faction}**.")
            else:
                await ctx.send(f"Weapon does not exist for **{faction}**.")
        else:
            await ctx.send("Invalid Faction.")


    @commands.command()
    @commands.has_any_role(506413971423625226, 506899380289142785, 548668450763964428)
    async def addweapon(self,ctx, faction: str, *, weapon: str):
        faction = faction.lower()
        if faction in factions:
            try:
                sql_con.execute(f"SELECT `weapons` FROM `data` WHERE name = '{faction}'")
                oldValue = sql_con.fetchone()[0]
            except:
                oldValue = ""

            oldValue += weapon + ","

            sql_con.execute(f"UPDATE 'data' SET 'weapons' = '{oldValue}' WHERE name = '{faction}'")
            sql_config.commit()
            await ctx.send(f"Faction **{faction}** now have **{oldValue}**.")
        else:
            await ctx.send("Invalid Faction.")


    @commands.command()
    @commands.has_any_role(506413971423625226, 506899380289142785, 548668450763964428)
    async def sendstats(self,ctx, channel: discord.TextChannel=None):
        if not channel:
            channel = ctx.channel
        # await channel.send("Faction\t\tCoins\t\tViking Loot\t\tPersian Loot\t\tRoman Loot\t\tEgyptian Root\t\tGreek Loot\t\tSamurai Loot\t\tWeapons")
        for result in sql_con.execute("SELECT * FROM `data`"):
            embed = discord.Embed(title="History Wars Leaderboard", colour=discord.Colour(0x66a44),
                                description=result[0].title() + ":",
                                timestamp=datetime.datetime.now())
            embed.set_footer(text="History Wars Bot",
                            icon_url="https://cdn.discordapp.com/icons/506407988794490880/1c8e309e868e86f430e7c3ecc9a56e09.jpg")

            weapons = result[8].replace(",", "\n").title()
            if len(weapons) <= 1:
                weapons = "No Weapons Yet"

            loot = f"Viking Loot: {result[2]}\n" + \
                f"Persian Loot: {result[3]}\n" + \
                f"Roman Loot: {result[4]}\n" + \
                f"Egyptian Loot: {result[5]}\n" + \
                f"Greek Loot: {result[6]}\n" + \
                f"Samurai Loot: {result[7]}"

            embed.add_field(name="Weapons:", value=weapons, inline=True)
            embed.add_field(name="Loot:", value=loot, inline=True)
            embed.add_field(name="Coins:", value=result[1], inline=True)
            # await ctx.send(embed=embed)
            await channel.send(embed=embed)


    @commands.command()
    @commands.has_any_role(506413971423625226, 506899380289142785, 548668450763964428)
    async def add(self,ctx, item: str, faction: str, amount: int):
        faction = faction.lower()
        item = item.lower()
        if faction in factions:
            if item in items:
                first = f"Adding **{item}** to **{faction}**, amount: **{amount}**."
                message = await ctx.send(first)
                try:
                    sql_con.execute(f"SELECT `{item}` FROM `data` WHERE name = '{faction}'")
                    oldValue = sql_con.fetchone()[0]
                except:
                    oldValue = 0

                sql_con.execute(f"UPDATE 'data' SET '{item}' = '{oldValue + amount}' WHERE name = '{faction}'")
                sql_config.commit()
                await message.edit(content=f"{first}\nNew value: **{oldValue + amount}**.")
            else:
                await ctx.send(
                    "Invalid Item.\nAvailable Items:\n\t-Viking_Loot\n\t-Persian_Loot\n\t-Roman_Loot\n\t-Egyptian_Loot\n\t-Greek_Loot\n\t-Samurai_Loot\n\t-Weapons\n\t-Coins")
        else:
            await ctx.send(
                "Invalid Faction.\nAvailable factions are: \n\t-Viking\n\t-Persian\n\t-Roman\n\t-Egyptian\n\t-Greek\n\t-Samurai")


    @commands.command()
    @commands.has_any_role(506413971423625226, 506899380289142785, 548668450763964428)
    async def resetdata(self,ctx):
        """RESETS DATA"""
        message = await ctx.send("*Processing...*")
        sql_con.execute("DROP TABLE IF EXISTS 'data'")
        await message.add_reaction("0\N{combining enclosing keycap}")

        sql_con.execute(
            "CREATE TABLE IF NOT EXISTS 'data' (name TEXT,coins INT DEFAULT 0," +
            "viking_loot INT DEFAULT 0," +
            "persian_loot INT DEFAULT 0," +
            "roman_loot INT DEFAULT 0," +
            "egyptian_loot INT DEFAULT 0," +
            "greek_loot INT DEFAULT 0," +
            "samurai_loot INT DEFAULT 0," +
            "weapons TEXT DEFAULT '')")
        sql_config.commit()
        await message.add_reaction("1\N{combining enclosing keycap}")

        sql_con.execute("INSERT INTO 'data' (name) VALUES ('viking')")
        sql_con.execute("INSERT INTO 'data' (name) VALUES ('persian')")
        sql_con.execute("INSERT INTO 'data' (name) VALUES ('roman')")
        sql_con.execute("INSERT INTO 'data' (name) VALUES ('egyptian')")
        sql_con.execute("INSERT INTO 'data' (name) VALUES ('greek')")
        sql_con.execute("INSERT INTO 'data' (name) VALUES ('samurai')")
        sql_config.commit()
        await message.add_reaction("2\N{combining enclosing keycap}")
        await message.add_reaction("\U0001F197")