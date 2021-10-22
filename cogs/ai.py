from discord.ext import commands
import time
import discord

class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool
        
    @commands.group()
    async def ai(self, ctx):
        if ctx.invoked_subcommand is None:
            return
        
    @ai.command()
    @commands.has_guild_permissions(administrator=True)
    async def connect(self, ctx):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM ai_channel WHERE channelid=%s",(ctx.channel.id,))
                if await c.fetchone() is None:
                    await c.execute("INSERT INTO ai_channel VALUES(%s)", (ctx.channel.id,))
                    await ctx.send("登録しました")
                else:
                    await ctx.send("登録済みです")
    
    @ai.command()
    async def ping(self, ctx):
        e=discord.Embed(title="ai ping測定", description="測定中...")
        m=await ctx.send(embed=e)
        t0 = time.monotonic()
        await self.talkapi(ctx.message)
        latency = (time.monotonic() - t0) * 1000
        e=discord.Embed(title="ai ping測定", description=f"{int(latency)}ms")
        await m.edit(embed=e)
                    
    @commands.Cog.listener(name="on_message")
    async def on_ai_message(self, message):
        if message.author.bot:
            return
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM ai_channel WHERE channelid=%s", (message.channel.id,))
                if not await c.fetchone() is None:
                    await message.add_reaction("🔄")
                    before = time.time()
                    content = await self.talkapi(message)
                    # print(round(time.time() - before, 1))
                    await message.remove_reaction("🔄", self.bot.user)
                    await message.channel.send(content)
        
    async def talkapi(self, message):
        data={
            "apikey": "DZZmBjFMWaoULWTbPbYAI2uoetySLfdR",
            "query": message.content
        }
        async with self.bot.session.post("https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk", data=data) as r:
            api=await r.json()
            return api['results'][0]['reply']
                
def setup(bot):
    bot.add_cog(ai(bot))
