from discord.ext import commands

class web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.template = bot.template
        
    @commands.route("/@me")
    async def me(self, request):
        return await self.template("index.html")