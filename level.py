from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, bot):
        self.pool = bot.pool
        self.bot = bot
        
    @commands.group()
    async def level(self, ctx):
        if ctx.invoked_subcommand is None:
            return
        
    @level.command()
    @commands.has_guild_permissions(administrator=True)
    async def set(self, ctx):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM level WHERE")