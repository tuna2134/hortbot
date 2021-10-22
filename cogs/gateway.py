from discord.ext import commands
import ujson

class Gateway(commands.Cog):
    def __init__(self, bot):
        @bot.web.websocket("/gateway")
        async def gateway(request, ws):
            while True:
                data = ujson.loads(await ws.recv())
                if data["t"] == "login":
                    if data["d"]["token"] == "token":
                        bot.ws_list.append(ws)

def setup(bot):
    bot.add_cog(Gateway(bot))