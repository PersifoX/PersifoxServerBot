"""
The main file-loader for the bot

supports:
- async input in terminal
- change status
- reload cogs without reload
- logging
- detection events:
  - resume
  - disconnect
  - connect
  - wrong token
  - stopped

Created by Persifox
"""

print("loading...")
print("-----------------------")

import disnake
import threading
import asyncio
import logging

from disnake.ext import commands
from colorama    import Fore, Style
from dotenv      import load_dotenv
from os          import getenv, listdir


load_dotenv(dotenv_path="statusx.env")


print(Fore.GREEN + "libs imported")
print("-----------------------")
print(f"Powered on {disnake.__name__} | version {disnake.__version__}")
print("-----------------------" + Fore.MAGENTA)



# Classes and logging

bot  = commands.Bot(command_prefix=commands.when_mentioned_or(getenv("PREFIX")), intents=disnake.Intents.all(), help_command=None, strip_after_prefix=True)
logging.basicConfig(level=logging.INFO, filename="statusx.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")

try:
    import utils.input as read
    read = read.Readinput(bot=bot)

except:
    print(Fore.RED + "Couldn't load tools. Check tool's folder")
    print("-----------------------" + Fore.MAGENTA)
    read = None

# funcs

if read:
    def forever(): # create async loop for listening input in console
        loop = asyncio.new_event_loop()
        loop.run_until_complete(read.readinput())
        loop.close()


def cogsLoad(self): # old, working without pycord
        curr, total = 1, len(listdir("./cogs")) - 4 # cogs - folder

        for filename in listdir("./cogs"):

            if filename.endswith(".py"):
                try: # load cog
                    self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"cog {filename} load, {curr}/{total}")

                except Exception as error: # something in cog wrong
                    print(f"error in cog {filename}, {curr}/{total} | {error}")
                    logging.error(f"cog filename not load: {error}")

                curr += 1 # + 1 for current amount

        print("-----------------------")


# load cogs

cogsLoad(bot)

# on_ready event

@bot.event
async def on_ready():

    print(Fore.CYAN + f"Starting as {bot.user} (ID: {bot.user.id})")
    print("-----------------------" + Style.RESET_ALL)
    print(Fore.GREEN + "Started!")
    print("-----------------------" + Style.RESET_ALL)

    await bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(type=disnake.ActivityType.streaming, name=f"persifox.space")) # change status how 🌙
    
    # starting listening input in console
    if read:
        threading.Thread(target=forever, name="CMD").start()
    

    print(Fore.LIGHTCYAN_EX + "Waiting for input")
    print("-----------------------" + Style.RESET_ALL)
    
    logging.info("bot ready")

# events

@bot.event
async def on_resumed():
    print(Fore.GREEN +  "-----------------------\nbot resumed\n-----------------------" + Style.RESET_ALL)
    logging.info("bot resumed")


@bot.event
async def on_disconnect():
    print(Fore.RED +  "-----------------------\nbot disconnected or connection failed\n-----------------------" + Style.RESET_ALL)
    logging.warning("bot disconnected")

@bot.event
async def on_connect():
    print(Fore.GREEN +  "-----------------------\nbot connected\n-----------------------" + Style.RESET_ALL)
    logging.info("bot connected")

# trying to start bot

try:
    bot.run(getenv("TOKEN"))
except:
    print(Fore.RED +  "-----------------------\nConnection failed\n-----------------------" + Style.RESET_ALL)
finally:
    print(Fore.YELLOW +  "-----------------------\nStopped\n-----------------------" + Style.RESET_ALL)
