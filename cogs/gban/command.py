from discord.ext import commands
import discord
from discord.ui import Button, View

class Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(name="gban")
    async def Gban(self, ctx):
        if ctx.invoked_subcommand:
            return
        
    @Gban.command(name="add")
    @commands.is_owner()
    async def Add(self, ctx, target:discord.User, *, reason):
        e = discord.Embed(title="GBAN執行", description="GBANを執行しますか？")
        view = View()
        view.add_item(Button(
            label="はい",
            custom_id="True",
            style=discord.ButtonStyle.success
        ))
        view.add_item(Button(
            label="いいえ",
            custom_id="False",
            style=discord.ButtonStyle.danger
        ))
        m = await ctx.send(embed=e, view=view)
        def check(com):
            return com.type == discord.InteractionType.component and com.message == m.id
        com = await self.bot.wait_for("interaction", check=check)
        if com.data["custom_id"] == "True":
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as c:
                    await c.execute("SELECT * FROM gban_user WHERE user=%s",(target.id,))
                    data = await c.fetchone()
                    if data is None:
                        await self.gban_start(target, reason)
                        await c.execute("INSERT INTO gban_user VALUES(%s,%s)", (target.id, reason))
                        e = discord.Embed(title="GBAN執行", description="執行しました")
                        await m.edit(embed=e)
                    else:
                        e = discord.Embed(title="GBAN執行", description="過去に執行しているためできませんでした。")
                        await m.edit(embed=e)
        else:
            e = discord.Embed(title="GBAN執行", description="キャンセルしました")
            await m.edit(embed=e)
    
    async def gban_start(self, user, reason):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                for name in channel.topic.splitlines():
                    if name.startswith("hb>gban"):
                        await guild.ban(user, reason)
                        e = discord.Embed(title="GBAN通知")
                        e.add_field(name="対象者", value=user.name)
                        e.add_field(name="対象者ID", value=user.id)
                        e.add_field(name="理由", value=reason)
                        await channel.send(embed = e)
        await self.bot.send_ws({
            "t": "GBAN",
            "d": {
                "user": user.id,
                "reason": reason
            }
        })