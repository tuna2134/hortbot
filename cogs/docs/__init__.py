from .status import Docs_status

def setup(bot):
    bot.add_cog(Docs_status(bot))