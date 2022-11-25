#---main components---

print("Loading...")
print("-----------")

import disnake
from disnake.ext import commands

from colorama import Fore, Style
from dotenv import load_dotenv
from os import getenv, listdir

load_dotenv() #load token-file

print(Fore.GREEN + "librares loaded")
print("-----------------------" + Fore.MAGENTA)

#---main class--------

bot = commands.Bot(command_prefix=commands.when_mentioned_or(getenv("PREFIX")), intents=disnake.Intents.all()) #slash command only OR when mentioned


def cogsLoad(self):
        curr, total = 0, len(listdir("./cogs")) - 3
        for filename in listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
                curr += 1
                print(f"cog {filename} loaded, {curr}/{total}")

        print("-----------------------" + Style.RESET_ALL)

cogsLoad(bot)


@bot.event
async def on_ready():
    
    print(Fore.CYAN + f"Bot avaible how {bot.user} (ID: {bot.user.id})")
    print("-----------------------" + Style.RESET_ALL)
    print(Fore.GREEN + "Bot is ready!")
    print("-----------------------" + Style.RESET_ALL)


bot.run(getenv("TOKEN"))