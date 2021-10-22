from discord.ext import commands
from discord import InteractionType

class Button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, com):
        if isinstance(com.type, InteractionType):
            self.bot.dispatch("on_button_click", com)

def setup(bot):
    bot.add_cog(Button(bot))