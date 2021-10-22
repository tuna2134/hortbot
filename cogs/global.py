from discord.ext import commands, tasks
import discord
import asyncio
from time import time

class Global(commands.Cog):
    def __init__(self, bot):
        self.pool = bot.pool
        self.bot = bot
        self.protect = {}
    
    @commands.group(name="gc")
    async def Global(self, ctx):
        if ctx.invoked_subcommand is None:
            return
        
    @Global.command(name="join")
    @commands.has_guild_permissions(administrator=True)
    async def gc_join(self, ctx, * ,name="offical"):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM gc WHERE channel=%s",(ctx.channel.id,))
                if (await c.fetchone()) is None:
                    await c.execute("INSERT INTO gc VALUES(%s, %s)", (name, ctx.channel.id))
                    await ctx.send("接続しました")
                else:
                    await ctx.send("すでに接続しています")
                    
    @Global.command(name="leave")
    async def gc_leave(self, ctx):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM gc WHERE channel=%s", (ctx.channel.id,))
                data = await c.fetchone()
                if not data is None:
                    await c.execute("DELETE FROM gc WHERE channel=%s", (ctx.channel.id,))
                    await ctx.send("退出しました")
                else:
                    await ctx.send("接続されていません")
                    
    @commands.Cog.listener(name="on_message")
    async def global_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(self.bot.prefix):
            return
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM gc WHERE channel=%s",(message.channel.id,))
                data = await c.fetchone()
                if data is None:
                    return
                if (await self.cooldown(message)):
                    return
                await message.add_reaction("🔄")
                name = data[0]
                await c.execute("SELECT * FROM gc WHERE name=%s", (name,))
                channels = await c.fetchall()
                for name, channelid in channels:
                    if not channelid == message.channel.id:
                        channel = await self.bot.fetch_channel(channelid)
                        ch_webhooks = await channel.webhooks()
                        webhook = discord.utils.get(ch_webhooks, name="hort-global-webhook")
                        if webhook is None:
                            webhook=await channel.create_webhook(name="hort-global-webhook")
                        files = []
                        for at in message.attachments:
                            files.append(await at.to_file())
                        m = await webhook.send(content=message.clean_content, username=f"{message.author.name} ({message.author.id})", avatar_url=message.author.avatar.url, files=files, wait=True)
                        await c.execute("INSERT INTO gclog VALUES(%s, %s, %s)", (message.id, m.channel.id, m.id))
                await message.remove_reaction("🔄", self.bot.user)
                await message.add_reaction("✅")
                await asyncio.sleep(5)
                await message.remove_reaction("✅", self.bot.user)
    
    @commands.Cog.listener(name="on_message_edit")
    async def global_edit(self, before, after):
        if after.content == before.content:
            return
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM gclog WHERE m=%s",(after.id,))
                data = await c.fetchall()
                if data is None:
                    return
                for m, ch, m2 in data:
                    channel = await self.bot.fetch_channel(ch)
                    ch_webhooks = await channel.webhooks()
                    webhook = discord.utils.get(ch_webhooks, name="hort-global-webhook")
                    await webhook.edit_message(message_id=m2, content=after.content)
                    
    @commands.Cog.listener(name="on_raw_message_delete")
    async def global_delete(self, payload):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM gclog WHERE m=%s",(payload.message_id,))
                data = await c.fetchall()
                if data is None:
                    return
                for m, ch, m2 in data:
                    channel = await self.bot.fetch_channel(ch)
                    ch_webhooks = await channel.webhooks()
                    webhook = discord.utils.get(ch_webhooks, name="hort-global-webhook")
                    await webhook.delete_message(int(m2))
                await c.execute("DELETE FROM gclog WHERE m=%s", (payload.message_id))
                
    async def cooldown(self, message):
        now = time()
        if message.author.id in self.protect:
            if round(now - self.protect[message.author.id], 1) < 2:
                await message.add_reaction("⚠️")
                return True
            else:
                self.protect[message.author.id] = now
                return False
        else:
            self.protect[message.author.id] = now
            return False

def setup(bot):
    bot.add_cog(Global(bot))