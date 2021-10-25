from discord.ext import commands
import discord

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("ban")
    async def _ban(self, ctx, user:discord.User, *, reason = None):
        await guild.ban(user, reason)
        await ctx.send(f"{user.name}をBANしました！")

    @commands.command("kick")
    async def _kick(self, ctx, member:discord.Member, *, reason = None):
        await member.kick(reason)
        await ctx.send(f"{member.name}をKICKしました！")

def setup(bot):
    bot.add_cog(Mod(bot))