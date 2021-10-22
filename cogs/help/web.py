from discord.ext import commands
import ujson
import urllib.parse
from sanic.response import json

class Helpweb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/help.json", "r") as f:
            self.data = bot.help
        bot.web.add_route(self.help_web, "/help")
        bot.web.add_route(self.help_category, "/help/<category>")
        bot.web.add_route(self.help_command, "/help/<category>/<cmd>")

    @commands.route("/help/reload")
    async def reloadhelp(self, request):
        with open("data/help.json", "r") as f:
            self.bot.help = ujson.load(f)
        return json({"message": "complete"})
        
    async def help_web(self, request):
        return await self.bot.template("help.html", data=self.data)
            
    async def help_category(self, request, category):
        return await self.bot.template("help_category.html", category=urllib.parse.unquote(category), data=self.data[urllib.parse.unquote(category)])
        
    async def help_command(self, request, category, cmd):
        return await self.bot.template("help_command.html", cmd=urllib.parse.unquote(cmd), data=self.data[category]["command"][urllib.parse.unquote(cmd)][1])