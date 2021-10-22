from discord.ext import commands
import discord

class Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(name="gban")
    async def Gban(self, ctx):
        if ctx.invoked_subcommand:
            return
        
    @Gban.command(name="add")
    async def Add(self, ctx, target:discord.User, *, reason):
        pass
    
    async def gban_start(self, user, reason):
        pass