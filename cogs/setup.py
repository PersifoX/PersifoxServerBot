#Импорт библиотек
import mysql, mysql.connector
import disnake
import mctools
import datetime

from disnake.ext       import commands
from disnake           import TextInputStyle
from mctools           import RCONClient
from dotenv            import load_dotenv
from os                import getenv

load_dotenv() #Загрузка токенов доступа

class SetupModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Адрес сервера",
                placeholder="Например, persifox.space",
                custom_id="text",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Порт rcon",
                placeholder="Например, 25575",
                custom_id="title",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Пароль rcon",
                placeholder="Важно! ДО 20 символов",
                custom_id="description",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Id роли, кто может выполнять команды",
                placeholder="Например, 1038078768092299274",
                custom_id="url",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(
            title="Добавить сервер",
            custom_id="create_send",
            components=components,
        )


    async def callback(self, inter: disnake.ModalInteraction):

        input=list(inter.text_values.values()) #Интеграция с SetupModal

        connect = mysql.connector.connect(
            host=getenv("BD_HOST"),
            user=getenv("BD_LOGIN"),
            password=getenv("BD_PASS"),
            database=getenv("BD_DATABASE")
        )

        cursor = connect.cursor() #Подключение к бд

        cursor.execute(f"""
        INSERT INTO servers_table (server_name, server_port, server_pass, guild_admin_role, discord_guild) VALUES ("{input[0]}", "{input[1]}", "{input[2]}", "{input[3]}", "{inter.guild.id}")
        """) #Значения

        connect.commit()  #Запись значений

        print(cursor.rowcount, "record succesful.") #Вывод в консоль для статистики и отладки

        await inter.send(f"""
        **Успешно!**
        ||```yaml
        Сервер - {input[0]}
        Порт   - {input[1]}
        Пароль - {input[2]}
        Роль   - {input[3]}

        Зарегистрировано на этот сервер:
         id:   {inter.guild.id}
         дата: {datetime.datetime.now()}
        ```||
        """, ephemeral=True)



class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="setup", description="Настройте свой сервер!")
    async def setup_(inter: disnake.AppCmdInter):
        await inter.response.send_modal(modal=SetupModal())

    @setup_.error
    async def error(self, ctx, error):
            await ctx.send(embed=disnake.Embed(
                title="⭕ | **Ошибка:**", description=f"```{error}```",
                colour=disnake.Colour.red(),
                timestamp=datetime.datetime.now()),
                ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))