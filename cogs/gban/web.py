from discord.ext import commands
from sanic.response import json

class GbanWeb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = bot.pool
        bot.web.add_route(self.Gban_Route, "/api/gban", methods=["POST", "GET"])
        
    async def Gban_Route(self, request):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                if request.method == "GET":
                    await c.execute("SELECT * FROM gban_user")
                    rjson = {
                        "status": "True",
                        "item": {
                            "gban": []
                        }
                    }
                    for user, reason in (await c.fetchall()):
                        rjson["item"]["gban"].append({
                            "user": str(user),
                            "reason": reason
                        })
                    return json(rjson)
                elif request.method == "POST":
                    user = request.json["user"]
                    await c.execute("SELECT * FROM gban_user WHERE user=%s",(int(user),))
                    data = await c.fetchone()
                    if data is None:
                        return json({
                            "status": "False",
                            "item": {
                                "message": "I can't found that user."
                            }
                        })
                    else:
                        user, reason = data[0], data[1]
                        return json({
                            "status": "True",
                            "item": {
                                "user": str(user),
                                "reason": str(reason)
                            }
                        })