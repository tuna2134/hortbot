from .web import Captcha_web
from .command import captcha_cmd

def setup(bot):
    bot.add_cog(Captcha_web(bot))
    bot.add_cog(captcha_cmd(bot))