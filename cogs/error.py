from discord.ext import commands
from sanic.exceptions import NotFound
import traceback
import discord
from sanic.response import text
from discord.ui import View, Button
from module.page import Embeds

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.web.error_handler.add(NotFound, self.notfound)
        
    async def notfound(self, request, exception):
        return await self.bot.template("404.html")
        
    @commands.Cog.listener(name="on_command_error")
    async def error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            description="コマンドが見つかりません"
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            description="引数が足りません"
        elif isinstance(error, commands.errors.MissingPermissions):
            description="権限が足りません"
        else:
            error="".join(traceback.TracebackException.from_exception(error).format())
            error_list = [error[i: i+1900] for i in range(0, len(error), 1900)]
            embeds = Embeds(self.bot)
            for msg in error_list:
                embeds.add_item(discord.Embed(title="エラー", description=f"```py\n{msg}```"))
            return await embeds.send(ctx.message)
        e=discord.Embed(title="エラー", description=description, color=0xff0000)
        view = View()
        view.add_item(Button(label="サポートサーバー", url="https://discord.gg/pzC8VgMMn8"))
        await ctx.send(embed=e)
        
def setup(bot):
    bot.add_cog(Error(bot))