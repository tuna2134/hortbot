from discord.ext import commands

class debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    async def debug(self, ctx):
        if not ctx.invoked_subcommand:
            return
        
    @debug.command(name="reload", ailias=["load"])
    async def cog_load(self, ctx, file):
        try:
            self.bot.load_extension(f"cogs.{file}")
            await ctx.send("📥loaded")
        except commands.ExtensionAlreadyLoaded:
            self.bot.reload_extension(f"cogs.{file}")
            await ctx.send("🔁reloaded")
            
def setup(bot):
    bot.add_cog(debug(bot))