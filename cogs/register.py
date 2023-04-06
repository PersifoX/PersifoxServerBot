import disnake
import hashlib
import mysql.connector

import utils.embeds as tools

from os                   import getenv
from disnake.ext          import commands
from disnake.ext.commands import Cog
from disnake              import TextInputStyle
from dotenv               import load_dotenv

load_dotenv(dotenv_path="statusx.env")

sql = "INSERT INTO " + getenv("TABLE") + " (username, password, discordid) VALUES (%s, %s, %s)"

print(getenv("USER"))

async def contodb():
  mydb = mysql.connector.connect(
  host=getenv("HOST"),
  user="bot",
  password=getenv("PASS"),
  database=getenv("DB")
  )
  
  mycursor = mydb.cursor()


tool = tools.Embed()

class MyModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Никнейм",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=40,
            ),
            disnake.ui.TextInput(
                label="Пароль",
                custom_id="pass",
                style=TextInputStyle.short,
                max_length=40,
            ),
            disnake.ui.TextInput(
                label="Пароль повторно",
                custom_id="try_pass",
                style=TextInputStyle.short,
                max_length=40,
            ),
        ]
        super().__init__(title="Зарегистрироваться", components=components)


    async def callback(self, inter: disnake.ModalInteraction):
        items = dict(inter.text_values.items())
        
        password = items["pass"].encode()
        password = hashlib.sha256(password).hexdigest()
        
        val = (str(items["name"]), str(password), str(inter.author.id))


        if items["pass"] != items["try_pass"]:
            await inter.send(embed=tool.type_embed("error", "Неверный повтор пароля"), ephemeral=True)

            return
        
        if len(items["pass"]) < 8:
            await inter.send(embed=tool.type_embed("error", "Пароль слишком короткий"), ephemeral=True)

            return
        

        try:
          
            await contodb()
            
            mycursor.execute(sql, val)

            mydb.commit()

        except Exception as exp:
            await inter.send(embed=tool.type_embed("error", f"что пошло не так: ````{exp}```"), ephemeral=True)

            return
        
        await inter.send(embed=tool.type_embed("success", f"Успешно! Ваш ник: `" + items["name"] + "`"), ephemeral=True)


class Reg(Cog):
    def __init__(self, bot: disnake):
        self.bot = bot

    
    @commands.slash_command(name="reg", description="зарегистрироваться в лаунчере")
    async def reg(inter: disnake.AppCmdInter):
        await inter.response.send_modal(modal=MyModal())
        

def setup(bot: commands.Bot):
    bot.add_cog(Reg(bot))