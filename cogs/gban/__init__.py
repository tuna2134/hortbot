from .command import Command
#from .web import Web

def setup(bot):
    bot.add_cog(Command(bot))