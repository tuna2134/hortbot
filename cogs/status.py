from discord.ext import commands, tasks
import psutil
import datetime
import time
from datetime import datetime, timedelta

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