from discord.ext import commands
import discord

class NewsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)

    @commands.group("news")
    async def _news(self, ctx):
        pass

    @_news.command("add")
    @commands.is_admin()
    async def _news_add(self, ctx, *, content):
        data = content.splitlines()
        name = self.randomname(10)
        description = "\n".join(i for i in data[1:])
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("INSERt INTO news VALUES(%s, %s, %s)", (name, data[0], description))
        embed = discord.Embed(title = data[0], descripti)
        await ctx.send(embed = embed)

    async def _create_news(self, data):
        for i in data[1:]:
            if i.startswith("##", "###"):
                
        discord.Embed(title = data[0], description = description)