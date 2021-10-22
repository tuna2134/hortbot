from discord.ext import commands
import io
import discord
import aiohttp

class screenshot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ss")
    @commands.cooldown(1, 60, type=commands.BucketType.user)
    async def Ss(self, ctx, url):
        e=discord.Embed(title="スクリーンショット", description="取得中")
        e.set_footer(text="Powered by Chrome")
        m=await ctx.send(embed=e)
        data = {
            "url": url,
            "password": "dms2021"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post('https://hortbot-screenshot.herokuapp.com/api', json=data) as r:
                file = discord.File(io.BytesIO(await r.read()), filename="ss.png")
                channel=self.bot.get_channel(878398355745669181)
                f=await channel.send(file=file)
                e = discord.Embed(title="スクリーンショット")
                e.set_image(url=f.attachments[0].url)
                e.set_footer(text="Powered by Chrome")
                await m.edit(embed=e)

def setup(bot):
    bot.add_cog(screenshot(bot))