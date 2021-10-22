from sanic import Sanic
import os
from sanic.response import *
from module.bot import HortBot
from sanic.log import logger
import discord
import time
from module.web_manager import web_manager
from discord.ui import View, Button
from datetime import datetime, timedelta

token = os.getenv("token")

# testの場合True そうじゃない時はFalse
mode = False

if mode:
    prefix = "h2?"
    token = os.getenv("token")
else:
    prefix = "hb?"
    token = os.getenv("token2")

intents = discord.Intents.all()
intents.typing = False

bot = HortBot(command_prefix = prefix, intents = intents, help_command = None)

bot.prefix = prefix
    
#準備
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(status=discord.Status.dnd,name="Now system is starting...", type=1))
    bot.load_extension("jishaku")
    bot.load_extension("module.button")
    for filename in os.listdir("cogs"):
        if not filename.startswith("_") and filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
        elif "." not in filename and filename != "__pycache__" and filename[0] != ".":
            bot.load_extension("cogs."+filename)
    logger.info("Bot is start.")
    logger.info(f"Time to start is {round(time.time() - before, 1)} seconds")
    channel=bot.get_channel(829990083725623326)
    times = datetime.now()
    times = times+timedelta(hours=9)
    e=discord.Embed(title="起動通知")
    e.add_field(name="起動時間", value=times.strftime('%Y/%m/%d %H:%M'))
    view = View()
    view.add_item(Button(label="ステータス", url="https://hortbot.f5.si/status"))
    await channel.send(embed=e, view=view)
    bot.dispatch("full_ready")

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    await bot.process_commands(message)
  
if __name__ == "__main__":
    before = time.time()
    bot.run(token, host="0.0.0.0", port=8080)
