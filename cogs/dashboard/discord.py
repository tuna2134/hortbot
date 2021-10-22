from discord.ext import commands, tasks

class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool
        self.update.start()
        
    @tasks.loop(minutes=5)
    async def update(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                for guild in self.bot.guilds:
                    await c.execute("DELETE FROM guild WHERE guildid=%s",(guild.id,))
                    await c.execute("INSERT INTO guild VALUES(%s)",(guild.id,))