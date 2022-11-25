import disnake
from disnake.ext import commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="help", description="помощь")
    async def республика(self, ctx):

        await ctx.send(
        embed = disnake.Embed(title=f'Спасибо за выбор PersifoxServerBot!',
         color=disnake.Colour.purple(),
          description=f"""
          Вас приветствует команда ***PersifoxTeam!***

          Теперь бот доступен для всех серверов, открытых для ***rcon***.

          Для настройки своего сервера используйте команду `setup`.

          PersifoxTeam никогда не будет использовать ваши конфидециальные данные, весь исходный код доступен на **[github](https://github.com/PersifoX/PersifoxServerBot)**.

          ```yaml
          1. Если вам нужно удалить свой сервер\n из базы данных, создайте тикет.\n
          2. Ввод сервера повторно не допускается и выдает ошибку.\n
          3. На один сервер дискорд предоставляется только одно подключение.\n
          4. Если вы ввели данные неправильно или вам нужно их изменить, создайте тикет для их дальнейших изменений.
          ```
          """),
        ephemeral=True
        )

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))