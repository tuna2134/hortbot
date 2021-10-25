from discord.ext import commands, tasks
import psutil
import datetime
import time
from datetime import datetime, timedelta
from sanic.response import json

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.template = bot.template
        self.data = {}
        self.edit.start()

    @commands.route("/status")
    async def status_web(self, request):
        dt = datetime.fromtimestamp(self.data["time"])
        dt = dt + timedelta(hours=9)
        return await self.template("status.html", data=self.data, time=dt.strftime('%Y-%m-%d %H:%M'))

    @commands.route("/api/status")
    async def status_api(self, request):
        return json({
            "status": "ok",
            "content": {
                "cpu": str(self.data["cpu"]),
                "memory": str(self.data["memory"]),
                "disk": str(self.data["disk"]),
                "ping": str(self.data["ping"]),
                "time": str(self.data["time"])
            }
        })
    
    @tasks.loop(minutes=5)
    async def edit(self):
        self.data["ping"] = round(self.bot.latency * 1000)
        self.data["cpu"] = psutil.cpu_percent(interval=1)
        self.data["memory"] = psutil.virtual_memory().percent
        self.data["disk"] = psutil.disk_usage('/').percent
        self.data["time"] = time.time()
        self.data["guild_count"] = len(self.bot.guilds)
        self.data["user_count"] = len(self.bot.users)

def setup(bot):
    bot.add_cog(Status(bot))