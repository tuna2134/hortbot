from discord.ext import commands
import discord

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.group("image")
    async def _image(self, ctx):
        pass

    @_image.command("neko")
    async def _image_neko(self, ctx):
        async with self.session.get("https://nekobot.xyz/api/image?type=neko") as r:
            api = await r.json()
        embed = discord.Embed(title = "NEKO IMAGE")
        embed.set_image(url = api["message"])
        embed.set_footer(text = "Powered by NekoBot Api")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Image(bot))