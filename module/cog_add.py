from discord.ext import commands
from copy import copy


class OnCogAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._default_add_cog = copy(self.bot.add_cog)
        self._default_remove_cog = copy(self.bot.remove_cog)
        self.bot.add_cog = self._add_cog
        self.bot.remove_cog = self._remove_cog

    def _add_cog(self, cog, **kwargs):
        self.bot.dispatch("cog_add", cog)
        return self._default_add_cog(cog, **kwargs)

    def _remove_cog(self, name):
        cog = self.bot.cogs[name]
        self.bot.dispatch("cog_remove", cog)
        return self._default_remove_cog(name)


def setup(bot):
    bot.add_cog(OnCogAdd(bot))