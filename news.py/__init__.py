from .command import NewsCommand

def setup(bot):
    bot.add_cog(NewsCommand(bot))