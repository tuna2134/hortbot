from discord.ui import View, Button
import discord

class Embeds:
    def __init__(self, bot):
        self.bot = bot
        self.now = 0
        self.embeds = []

    def add_item(self, embed:discord.Embed):
        self.embeds.append(embed)

    async def button_edit(self):
        def check(com):
            return com.type == discord.InteractionType.component
        while True:
            com = await self.bot.wait_for("interaction", check=check)
            if com.data["custom_id"] in ["page_sys_left", "page_sys_right", "page_sys_stop"]:
                if com.message.id == self.message:
                    if com.data["custom_id"] == "page_sys_left":
                        will = self.now - 1
                        if will == 0:
                            return
                        embed = self.embeds[will]
                        await com.message.edit(embed=embed)
                        self.now = will
                    elif com.data["custom_id"] == "page_sys_right":
                        will = self.now + 1
                        embed = self.embeds[will]
                        await com.message.edit(embed=embed)
                        self.now = will
                    else:
                        view = View()
                        view.add_item(Button(label="<<", custom_id="page_sys_left", disabled=True))
                        view.add_item(Button(label="⏸", custom_id="page_sys_stop", disabled=True))
                        view.add_item(Button(label=">>", custom_id="page_sys_right", disabled=True))
                        await com.message.edit(view=view)
                        break

    async def send(self, message):
        view = View()
        view.add_item(Button(label="<<", custom_id="page_sys_left"))
        view.add_item(Button(label="⏸", custom_id="page_sys_stop"))
        view.add_item(Button(label=">>", custom_id="page_sys_right"))
        m = await message.channel.send(embed = self.embeds[0], view=view)
        self.message = m.id
        await self.button_edit()