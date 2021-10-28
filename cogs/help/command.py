from discord.ext import commands
import discord
import ujson
#import json

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/help.json", "r") as f:
            self.bot.help = ujson.load(f)
        self.data = bot.help
        self.url = "https://hortbot.f5.si/help"
        
    @commands.command()
    async def help(self, ctx, cmd=None):
        title, d = None, None
        if cmd:
            if cmd in self.data:
                title = f"ヘルプ カテゴリー:{cmd}"
                d = f"{self.url}/{cmd}"
            else:
                for i in self.data:
                    for e in self.data[i]["command"]:
                        if e == cmd:
                            title = f"ヘルプ コマンド:{cmd}"
                            d = f"{self.url}/{i}/{e}"
                            break
        else:
            title = "ヘルプ"
            d = self.url
        embed = discord.Embed(title=title, description=d)
        embed.set_footer(text="hb?help <カテゴリー/コマンド>で詳しいヘルプが見れます")
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_owner()
    async def reload_help(self, ctx):
        with open("data/help.json", "r") as f:
            self.data = ujson.load(f)
        await ctx.send("読み込み完了しました")
        
    @commands.command()
    async def dhelp(self, ctx, cmd=None):
        title, description = None, None
        if cmd:
            if cmd in self.data:
                title = f"ヘルプ カテゴリー:{cmd}"
                description = "\n".join(f"`{key}`-{self.data[cmd]['command'][key][0]}" for key in self.data[cmd]["command"])
            else:
                for i in self.data:
                    for e in self.data[i]["command"]:
                        if e == cmd:
                            title = f"ヘルプ コマンド:{cmd}"
                            description = self.data[i]["command"][cmd][1]
                            break
        else:
            title = "ヘルプ"
            description = "\n".join(f"`{cate}`-{self.data[cate]['description']}" for cate in self.data)
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(text="hb?dhelp <カテゴリー/コマンド>で詳しいヘルプが見れます")
        await ctx.send(embed=embed)