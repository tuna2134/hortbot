from discord.ext import commands
import discord

class Button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.component:
            self.bot.dispatch("button_click", interaction)

def setup(bot):
    bot.add_cog(Button(bot))