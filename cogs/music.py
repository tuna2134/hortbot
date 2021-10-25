from discord.ext import commands
import niconico_dl
from discord.ui import View, Button

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #実験していない
    @commands.command("play")
    async def _play(self, ctx, url):
        channel = ctx.author.voice.channel
        if channel is None:
            await ctx.send("VCに接続してください")
        if ctx.voice_client is None:
            await channel.connect()
        async with niconico_dl.NicoNicoVideoAsync(url, loop=self.bot.loop, log=True) as nico:
            ctx.voice_client.play(nico.get_download_link)
            data = await nico.get_info()
            await ctx.send(f'{data["video"]["title"]}を再生しました')

    # まだ作成中
    @commands.command("search_play")
    async def _search_play(self, ctx, *, word):
        query = {
            "q": word,
            "_sort": "-viewCounter",
            "targets": "title",
            "fields": "contentId,title,viewCounter"
        }
        async with self.bot.session.get("https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search", params=query) as r:
            data = await r.json()
            view = View()
            select = Select(custom_id="nicosearch")
            for i in data["data"][:5]:
                title = i["title"]
                contentId = i["contentId"]
                select.add_option(label=title)
            view.add_item(select)
            e = discord.Embed(title="曲を選択してください")
            m = await ctx.send(embed=e, view=view)
            def check(com):
                com.type == discord.InteractionType.component
            com = await self.bot.wait_for("interaction", check=check)
            if com.data["custom_id"] == "nicosearch":
                await m.edit(f"test\n{com.data}")
                

def setup(bot):
    bot.add_cog(music(bot))