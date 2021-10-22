from discord.ext import commands
from sanic.response import text
from sanic.exceptions import SanicException
import os
import time
from module.oauth import Oauth
import os
import aiohttp

class Captcha_web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool
        self.sitekey = os.getenv("sitekey")
        self.oauth = Oauth()
        bot.web.add_route(self.verify, "/verify/<name>", methods=["GET","POST"])
        self.secret_key = os.getenv("secret_key")

    @commands.route("/verify/callback")
    async def verify_callback(self, request):
        return await self.oauth.callback(request)
        
    async def verify(self, request, name=None):
        user = await self.oauth.get_user(request)
        if request.method == "GET":
            async with self.pool.acquire() as conn:
                async with conn.cursor() as c:
                    await c.execute("SELECT * FROM captcha_url WHERE url=%s", (name,))
                    data = await c.fetchone()
            if data is None:
                raise SanicException("存在しないぞお", 400)
            if round(time.time() - float(data[2])) > 600:
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as c:
                        await c.execute("DELETE FROM captcha_url WHERE url=%s", (name,))
                raise SanicException("時間切れ", 400)
            return await self.bot.template("verify.html", sitekey=self.sitekey, name=name, user=user.get("id"))
        else:
            rjson={
                "secret": self.secret_key,
                "response": request.form["h-captcha-response"]
            }
            async with aiohttp.ClientSession() as session:
                async with session.post("https://hcaptcha.com/siteverify", data=rjson) as response:
                    data=await response.json()
                    if data["success"] == True:
                        async with self.pool.acquire() as conn:
                            async with conn.cursor() as c:
                                await c.execute("SELECT * FROM captcha_url WHERE url=%s", (name,))
                                name, guildid, time_ = await c.fetchone()
                                await c.execute("SELECT * FROM captcha_web WHERE guildid=%s", (guildid,))
                                guildid, channelid, roleid = await c.fetchone()
                                guild = self.bot.get_guild(int(guildid))
                                print(guild.name)
                                role = guild.get_role(int(roleid))
                                member = await guild.fetch_member(int(user["id"]))
                                print(member.id)
                                print(role.id)
                                print(guild.id)
                                await member.add_roles(role, reason="認証に成功したため")
                                await c.execute("DELETE FROM captcha_url WHERE url=%s", (name,))
                        return await self.bot.template("verified.html")
                    else:
                        return await self.bot.template("verify.html", user=user.get("id"), sitekey=self.sitekey, name=name)