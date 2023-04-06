import datetime

from os       import listdir
from colorama import Fore, Style

class Readinput():
    def __init__(self, bot):
        self.bot = bot

    def cogsReload(self, bot):
            print(Fore.CYAN + "-----------------------")
            curr, total = 0, len(listdir("./cogs")) - 2
            for filename in listdir("./cogs"):
                if filename.endswith(".py"):
                    bot.reload_extension(f"cogs.{filename[:-3]}") 
                    curr += 1
                    print(f"cog {filename} reload, {curr}/{total}")

            print("-----------------------" + Style.RESET_ALL)


    async def readinput(self):

        while True:
            
            read = input(">")

            if read == "cogsreload":
                self.cogsReload(self.bot)

            elif read == "help":
                print(Fore.GREEN + """
    cogsreload - reload all cogs
    stop       - disconnecting bot and close session
    info       - get info from discord
    switch     - switch token
    clear      - clear cache
                                        """ + Style.RESET_ALL)

            elif read == "stop":
                print(Fore.YELLOW + "disconnecting..." + Style.RESET_ALL)
                exit()


            elif read == "reload":
                print(Fore.YELLOW + "clearing..." + Style.RESET_ALL)
                self.bot.clear()
                print(Fore.GREEN + "done" + Style.RESET_ALL)
                
            elif read == "switch":
                await self.bot.start(token=input(Fore.CYAN + "token\n" + Style.RESET_ALL + ">>>"))


            elif read == "info":
                print(Fore.GREEN + f"""
    bot name: {self.bot.user}  | id: {self.bot.user.id}
    owner:    {self.bot.owner} | id: {self.bot.owner_id}
    status:   {self.bot.status}
    limit:    {self.bot.session_start_limit.reset_time}
    ============================================
    guilds:   {len(self.bot.guilds)}
    users:    {len(self.bot.users)}
    emojis:   {len(self.bot.emojis)}
    stickers: {len(self.bot.stickers)}
    ----------------
    {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}
                """ + Style.RESET_ALL)
            
            else:
                print(Fore.YELLOW + "unknow command. Type 'help' for get info about commands" + Style.RESET_ALL)