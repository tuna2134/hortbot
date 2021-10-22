from discord.ext import commands, tasks
import discord
import random, string
import time
from discord.ui import View, Button

class captcha_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool
        self.Captcha_web_reset.start()
        
    def randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)

    @tasks.loop(minutes=5)
    async def Captcha_web_reset(self):
        async with self.bot.db.cursor() as c:
            await c.execute("SELECT * FROM captcha_url")
            for url, guild, times in (await c.fetchall()):
                times = float(times)
                if round(time.time() - times) > 600:
                    print(f"reset a url:{url}")
                    await c.execute("DELETE FROM captcha_url WHERE url=%s",(url,))
        
    @commands.group(name="captcha")
    async def captcha(self, ctx):
        pass
    
    @captcha.command(name="web")
    @commands.has_guild_permissions(administrator=True)
    async def web(self, ctx, role:discord.Role):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("INSERT INTO captcha_web VALUES(%s,%s,%s);", (int(ctx.guild.id), int(ctx.channel.id), int(role.id)))
        await ctx.send("登録しました")
        
    @captcha.command(name="image")
    @commands.has_guild_permissions(administrator=True)
    async def image(self, ctx, role:discord.Role):
        view = View()
        view.add_item(Button(label="認証", custom_id="auth_image"))
        e = discord.Embed(title="画像認証", description="認証をクリックしてください")
        m = await ctx.send(embed=e, view=view)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("INSERT INTO captcha_image VALUES(%s, %s, %s)", (m.channel.id, m.id, role.id))

    @captcha.command(name="create")
    async def create(self, ctx):
        name = self.randomname(10)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM captcha_web WHERE guildid=%s", (ctx.guild.id,))
                data = await c.fetchone()
                if data is None:
                    return
                await c.execute("INSERT INTO captcha_url VALUES(%s,%s,%s);", (name, ctx.guild.id, str(time.time())))
        url = "https://hortbot.f5.si/verify/"+name
        embed=discord.Embed(title="web認証", description=f"ここで認証してください\n{url}")
        await ctx.send(embed=embed)
        
    @commands.Cog.listener(name="on_button_click")
    async def send_image(self, com):
        if com.data["custom_id"] == "auth_image":
            number = self.randomname(5)
            await com.response.pong()
        
    @commands.Cog.listener(name="on_member_join")
    async def captcha_send(self, member):
        guildid = member.guild.id
        name = self.randomname(20)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM captcha_web WHERE guildid=%s", (guildid,))
                data = await c.fetchone()
                if data is None:
                    return
                await c.execute("INSERT INTO captcha_url VALUES(%s,%s,%s);", (name, guildid, str(time.time())))
        channelid = data[1]
        url = "https://hortbot.f5.si/verify/"+name
        channel = await self.bot.fetch_channel(channelid)
        embed=discord.Embed(title="web認証", description=f"ここで認証してください\n{url}")
        await channel.send(embed=embed)
