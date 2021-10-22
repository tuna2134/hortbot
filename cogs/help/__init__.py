from .command import Help
from .web import Helpweb

def setup(bot):
    bot.add_cog(Help(bot))
    bot.add_cog(Helpweb(bot))