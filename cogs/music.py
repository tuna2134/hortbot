from discord.ext import commands
import niconico_dl
from discord.ui import View, Button, Select
import discord

BEFORE_OPTIONS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
OPTIONS = "-vn"

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get(self, nico):
        return discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(
                await nico.get_download_link(),
                before_options=BEFORE_OPTIONS,
                options=OPTIONS
            )
        )

    #実験していない
    @commands.command("play")
    async def _play(self, ctx, url):
        channel = ctx.author.voice.channel
        if channel is None:
            await ctx.send("VCに接続してください")
        if ctx.voice_client is None:
            await channel.connect()
        async with niconico_dl.NicoNicoVideoAsync(url, loop=self.bot.loop, log=True) as nico:
            ctx.voice_client.play(await self.get(nico))
            data = await nico.get_info()
            await ctx.send(f'{data["video"]["title"]}を再生しました')

    @commands.command("pause")
    async def _pause(self, ctx):
        discord.VoiceClient.pause()
        await ctx.send("一時停止しました")

    @commands.command("search_play")
    async def _search_play(self, ctx, *, word):
        channel = ctx.author.voice.channel
        if channel is None:
            await ctx.send("VCに接続してください")
        if ctx.voice_client is None:
            await channel.connect()
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
                contentId = i["contentId"]
                title = i["title"] + f" {contentId}"
                select.add_option(label=title)
            view.add_item(select)
            e = discord.Embed(title="曲を選択してください")
            m = await ctx.send(embed=e, view=view)
            def check(com):
                return com.type == discord.InteractionType.component
            com = await self.bot.wait_for("interaction", check=check)
            if com.data["custom_id"] == "nicosearch":
                _id = com.data["values"][0].split()[-1]
                async with niconico_dl.NicoNicoVideoAsync(f"https://www.nicovideo.jp/watch/{_id}", loop=self.bot.loop, log=True) as nico:
                    ctx.voice_client.play(await self.get(nico))
                    data = await nico.get_info()
                    await m.edit(f'{data["video"]["title"]}を再生しました')

def setup(bot):
    bot.add_cog(music(bot))