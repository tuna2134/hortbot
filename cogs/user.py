from discord.ext import commands
from datetime import datetime, timedelta
from module.web_manager import web_manager

class User(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        bot.web.add_route(self.user_web, "/user_info", methods=["GET","POST"])
        self.web_manager = web_manager()
    
    async def user_web(self, request):
        if request.method == "GET":
            if self.web_manager.cooldown(request, 5):
                return await self.bot.template("429.html")
            return await self.bot.template("user_info.html")
        else:
            userid = request.form.get("userid")
            try:
                user = await self.bot.fetch_user(userid)
            except:
                return await self.bot.template("user_error.html")
            else:
                avatar=user.avatar.replace(format="png").url
                ct=user.created_at+timedelta(hours=9)
                return await self.bot.template("user_info_result.html", user=user, avatar=avatar, create_time=ct.strftime('%Y-%m-%d'))
            
def setup(bot):
    bot.add_cog(User(bot))