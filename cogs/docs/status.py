from discord.ext import commands
from sanic.response import redirect

class Docs_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.template = bot.template

    @commands.route("/docs")
    async def docs_main(self, request):
        return redirect("/docs/main")

    @commands.route("/docs/<name>")
    async def docs_content(self, request, name):
        try:
            with open(f"templates/docs/{name}.md", mode="r") as f:
                content = f.read()
        except FileNotFoundError:
            return await self.template("404.html")
        else:
            return await self.template("docs/layout.html", content=content)