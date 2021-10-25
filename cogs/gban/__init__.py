from .command import Command
from .web import GbanWeb

def setup(bot):
    bot.add_cog(Command(bot))
    bot.add_cog(GbanWeb(bot))