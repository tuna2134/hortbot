from discord.ext import commands
from sanic.response import redirect

class web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.template = bot.template
        
    @commands.route("/login")
    async def login(self, request):
        return redirect("/docs")

    @commands.route("/me")
    async def me(self, request):
        return await self.template("dashboard/main.html")