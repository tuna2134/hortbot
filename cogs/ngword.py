from discord.ext import commands
import discord
import asyncio

class Ngword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool

    @commands.group(name="ngword")
    async def Ngword(self, ctx):
        if ctx.invoked_subcommand:
            return

    @Ngword.command(name="add")
    @commands.has_guild_permissions(administrator=True)
    async def Add(self, ctx, *, word):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM ngword WHERE guild=%s AND word=%s",(ctx.guild.id, word))
                if not await c.fetchone() is None:
                    return await ctx.send("既に登録済みです")
                await c.execute("INSERT INTO ngword VALUES(%s,%s)",(ctx.guild.id, word))
                await ctx.send("登録しました")

    @Ngword.command(name="remove")
    @commands.has_guild_permissions(administrator=True)
    async def Remove(self, ctx, *, word):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM ngword WHERE guild=%s AND word=%s",(ctx.guild.id, word))
                if await c.fetchone() is None:
                    return await ctx.send("登録されていません")
                await c.execute("DELETE FROM ngword WHERE guild=%s AND word=%s",(ctx.guild.id, word))
                await ctx.send("リストから削除しました")

    @Ngword.command(name="list")
    @commands.has_guild_permissions(administrator=True)
    async def List(self, ctx):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM ngword WHERE guild=%s",(ctx.guild.id,))
                data = await c.fetchall()
                if data is None:
                    return await ctx.send("一つも登録されてないので表示できません")
                d="\n".join(word for guild, word in data)
                e=discord.Embed(title="NGWORD LIST", description=d)
                await ctx.send(embed=e)

    @commands.Cog.listener(name="on_message")
    async def Ngmessage(self, message):
        if message.author.bot:
            return
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM ngword WHERE guild=%s",(message.guild.id,))
                for guild, word in await c.fetchall():
                    if word in message.content:
                        await message.delete()
                        e = discord.Embed(title="NGWORD機能",description="NGWORDに登録されているワードを発言したため削除しました")
                        e.set_footer(text="5秒後に消えます")
                        m = await message.channel.send(embed=e)
                        await asyncio.sleep(5)
                        await m.delete()

def setup(bot):
    bot.add_cog(Ngword(bot))