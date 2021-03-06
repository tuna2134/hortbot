from discord.ext import commands, tasks
import time
import discord
import random

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool
        self.loop.start()
        
    @commands.group(name="giveaway")
    async def Giveaway(self, ctx):
        if ctx.invoked_subcommand:
            return
        
    @Giveaway.command(name="set")
    async def set(self, ctx, times_:float, *, item):
        time_=times_ * 60 + time.time()
        embed=discord.Embed(title="GIVEAWAY",description=f"πγ«γͺγ’γ―γ·γ§γ³γγ¦εε οΌ\nζ―ε:{item}")
        embed.set_footer(text=f"{times_}εεΎγ«η΅γγγΎγ")
        m=await ctx.send(embed=embed)
        await m.add_reaction("π")
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("INSERT INTO giveaway VALUES(%s,%s,%s)",(m.channel.id,m.id,str(time_)))
                
    @tasks.loop(minutes=1)
    async def loop(self):
        now = time.time()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM giveaway")
                for channel, message, time_ in await c.fetchall():
                    if now > float(time_):
                        channel = await self.bot.fetch_channel(channel)
                        message = await channel.fetch_message(message)
                        users = await message.reactions[0].users().flatten()
                        users.remove(await self.bot.fetch_user(self.bot.user.id))
                        try:
                            winner = random.choice(users)
                        except:
                            winner = "εε θγͺγ"
                        embed = discord.Embed(title="GIVEAWAYη΅δΊ", description=f"εθ:{winner.mention}")
                        await message.edit(embed=embed)
                        await c.execute("DELETE FROM giveaway WHERE message=%s",(message.id,))
                        
def setup(bot):
    bot.add_cog(giveaway(bot))