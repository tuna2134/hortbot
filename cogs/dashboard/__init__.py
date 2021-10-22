from .discord import Discord
from .web import web

def setup(bot):
    bot.add_cog(Discord(bot))
    bot.add_cog(web(bot))