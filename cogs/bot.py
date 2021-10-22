from discord.ext import commands, tasks
from sanic.response import json, redirect
import psutil
import discord
from discord.ui import Button

class View(discord.ui.View):
    def __init__(self):
        super().__init__()

class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.web.add_route(self.main, "/")
        #bot.web.add_route(self.status, "/status")
        bot.web.add_route(self.game, "/game")
        self.change.start()
        
    async def game(self, request):
        return await self.bot.template("game.html")
    
    async def main(self, request):
        return await self.bot.template("index.html")
        
    @commands.route("/test", methods=["POST", "GET"])
    async def test(self, request):
        return json({"hello": "world"})
        
    @tasks.loop(minutes=5)
    async def change(self):
        await self.bot.change_presence(activity=discord.Activity(name=f"{self.bot.prefix}help | {len(self.bot.guilds)}server's", type=discord.ActivityType.watching))
         
    @commands.command()
    async def ping(self, ctx):
        e=discord.Embed(title="ping測定", description=f"{round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=e)
        
    @commands.command()
    @commands.is_owner()
    async def manage_db(self, ctx, *, word):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as conn:
                await conn.execute(word)
                if word.upper().startswith("SELECT"):
                    await ctx.send(await conn.fetchall())
                else:
                    await ctx.send("完了")
                    
    @commands.command()
    async def thanks(self, ctx):
        e=discord.Embed(title="thanks")
        e.add_field(name="陸ステップネットワーク", value="MySQLサーバーを借りています")
        view = View()
        view.add_item(Button(label="公式サイト", url="https://www.risupunet.jp"))
        await ctx.send(embed=e, view=view)
        
    @commands.command()
    async def about(self, ctx):
        e=discord.Embed(title="BOTに関すること")
        e.add_field(name="BOTのオーナー", value="DMS")
        e.add_field(name="WEBの開発者", value="mf_Mii")
        e.add_field(name="BOTの開発者", value="孤独のコーヒー")
        e.add_field(name="モデレーター", value="kazuma")
        e.add_field(name="BOTの導入数", value=len(self.bot.guilds))
        view = View()
        view.add_item(Button(label="サポートサーバー", url="https://discord.gg/pzC8VgMMn8", style=discord.ButtonStyle.green))
        view.add_item(Button(label="公式サイト", url="https://hortbot.f5.si", style=discord.ButtonStyle.green))
        await ctx.reply(embed=e, view=view)

    @commands.Cog.listener("on_message")
    async def message(self, message):
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
            return
        #await self.bot.process_commands(message)

    @commands.route("/favicon.ico")
    async def favicon(self, request):
        return redirect("/static/image/favicon.ico")
        
def setup(bot):
    bot.add_cog(Bot(bot))