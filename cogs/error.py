from discord.ext import commands
from sanic.exceptions import NotFound
import traceback
import discord
from sanic.response import text
from discord.ui import View, Button

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
            description=f"```py\n{error[-1990:]}```"
        e=discord.Embed(title="エラー", description=description, color=0xff0000)
        view = View()
        view.add_item(Button(label="サポートサーバー", url="https://discord.gg/pzC8VgMMn8"))
        await ctx.send(embed=e)
        
def setup(bot):
    bot.add_cog(Error(bot))