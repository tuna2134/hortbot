from discord.ext import commands
import aiohttp
from asyncio import sleep
import discord

class Covid19(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command(name="covid19", aliases=["c19"])
    async def _covid19(self, ctx, kuni="日本"):
        e = discord.Embed(title=f"covid19:{kuni}", description="取得中... 🔄")
        e.set_footer(text="Powered by japan government.")
        m = await ctx.send(embed=e)
        async with self.session.get("https://opendata.corona.go.jp/api/OccurrenceStatusOverseas") as r:
            data = await r.json()
            e = discord.Embed(title=f"covid19:{kuni}")
            for i in data["itemList"]:
                if i["dataName"] == kuni:
                    found = True
                    e.add_field(name="感染者数", value=i["infectedNum"])
                    e.add_field(name="死亡者数", value=i["deceasedNum"])
                    e.set_footer(text=i["date"])
                    break
            if not found:
                return await m.edit("見つかりませんでした")
        await m.edit(embed=e)

def setup(bot):
    bot.add_cog(Covid19(bot))