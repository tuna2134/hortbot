from discord.ext import commands
import discord

class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool

    @commands.command("afk")
    async def _afk(self, ctx, *, reason="なし"):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM afk user=%s", (ctx.author.id,))
                if (await c.fetchone()) is None:
                    await c.execute("INSERT INTO afk VALUES(%s, %s)", (ctx.author.id, reason))
                    await ctx.send("AFKを設定しました。")
                else:
                    await c.execute("DELETE FROM afk WHERE user=%s", (ctx.author.id,))
                    await ctx.send("AFKを解除しました。")

        @commands.Cog.listener("on_message")
        async def _afk_message(self, message):
            if message.author.bot:
                return
            async with self.pool.acquire() as conn:
                async with conn.cursor() as c:
                    await c.execute("SELECT * FROM afk WHERE user=%s", (message.author.id,))
                    if not (await c.fetchone()) is None:
                        e = discord.Embed(title="AFK機能", description="解除しました")
                        await message.reply(embed = e)
                    else:
                        for user in message.mentions:
                            await c.execute("SELECT * FROM afk WHERE user=%s", (user.id,))
                            data = await c.fetchone()
                            if data is None:
                                return
                            else:
                                e = discord.Embed(title="AFK機能", description=f"理由:{data[1]}")
                                await message.reply(embed = e)

def setup(bot):
    bot.add_cog(Afk(bot))