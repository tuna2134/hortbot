from discord.ext import commands
from module.page import Embeds
from discord import Embed
from contextlib import redirect_stdout
import textwrap
import traceback
import io
import os

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("page_test")
    async def _page_test(self, ctx):
        embeds = Embeds(self.bot)
        embeds.add_item(Embed(title="Test", description="Page1"))
        embeds.add_item(Embed(title="Test", description="Page2"))
        await embeds.send(ctx.message)

    @commands.group("debug")
    async def _debug(self, ctx):
        if ctx.invoked_subcommand:
            pass

    @_debug.command("reload")
    async def _debug_reload(self, ctx):
        self.bot.web.router.reset()
        for filename in os.listdir("cogs"):
            if not filename.startswith("_") and filename.endswith(".py"):
                self.bot.reload_extension(f"cogs.{filename[:-3]}")
            elif "." not in filename and filename != "__pycache__" and filename[0] != ".":
                self.bot.reload_extension("cogs."+filename)
        self.bot.web.router.finalize()

    @_debug.command("eval")
    async def _debug_eval(self, ctx, *, body):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }
        env.update(globals())
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        exec(to_compile, env)
        func = env['func']
        try:
            with redirect_stdout(stdout):
                result = await func()
        except Exception as msg:
            error = traceback.format_exc()
            msg_list = [error[i: i+1900] for i in range(0, len(error), 1900)]
            embeds = Embeds(self.bot)
            for meg in msg_list:
                embeds.add_item(Embed(title="Error", description=meg))
            await embeds.send(ctx.message)
        else:
            value = stdout.getvalue()
            if value == "":
                return
            msg_list = [value[i: i+1900] for i in range(0, len(value), 1900)]
            embeds = Embeds(self.bot)
            print(len(msg_list))
            for msg in msg_list:
                embeds.add_item(Embed(title="result", description=f"```\n{msg}```"))
            await embeds.send(ctx.message)

def setup(bot):
    bot.add_cog(Debug(bot))