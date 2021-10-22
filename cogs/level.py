from discord.ext import commands, tasks
import aiomysql

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now = {}
        self.pool = bot.pool
        #self.guilds = []

    @commands.Cog.listener()
    async def on_full_ready(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM level_setup")
                self.guilds = [guild[0] for guild in (await c.fetchall())]
                print(self.guilds)

    @commands.command("level")
    async def level(self, ctx, bool:bool=True):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                if bool:
                    if not ctx.guild.id in self.guilds:
                        await c.execute("INSERT INTO level_setup VALUES(%s)", (ctx.guild.id,))
                        self.guilds.append(ctx.guild.id)
                    else:
                        return await ctx.send("設定済みです")
                else:
                    await c.execute("DELETE FROM level_setup WHERE guild=%s", (ctx.guild.id,))
                    self.guilds.append(ctx.guild.id)
        await ctx.send("設定しました")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild.id in self.guilds:
            return
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM level WHERE author=%s",(message.author.id))
                data = await c.fetchone()
                if data is None:
                    await c.execute("INSERT INTO level VALUES(%s,%s,%s,%s)",(message.guild.id,message.author.id,1,1))
                else:
                    guild, user, level, exp = data
                    if exp+1 >= level*3:
                        print(level+1)
                        await c.execute("UPDATE level SET level=%s AND exp=%s WHERE author=%s",(level+1,1,message.author.id))
                        await message.channel.send("レベルアップしました")
                    else:
                        await c.execute("UPDATE level SET exp=%s WHERE author=%s",(exp+1,message.author.id))
            
def setup(bot):
    bot.add_cog(level(bot))