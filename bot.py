import discord, asyncio, logging
from discord.ext import commands
import time
import sys

bot = commands.Bot(command_prefix='+',description="Made by MrEdinLaw (leaderboard) and JdavisBro (raid)")
appinfo = None
logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)
extensions = ['owner','raid','leaderboard']
bot.startTime = time.time()

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            logging.warning("{} was unable to be loaded.".format(extension))
            raise
        else:
            logging.info("{} loaded.".format(extension))

@bot.event
async def on_ready():
    logging.info("Logged in as {} with ID: {}".format(bot.user,bot.user.id))
    await bot.change_presence(status=discord.Status.online,activity=discord.Game("on History Wars!"))
    global appinfo
    appinfo = await bot.application_info()
    logging.info("Hello {}".format(appinfo.owner))

bot.run(sys.argv[1])