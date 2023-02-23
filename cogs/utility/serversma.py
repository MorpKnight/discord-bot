import discord
from discord.ui import Button, View
from discord.utils import get


class games(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
    
    @discord.ui.button(
        label = "Genshin Impact",
        style = discord.ButtonStyle.blurple,
        custom_id = "Genshin Impact",
        emoji = "<:genshin:815419235748544564>"
    )
    async def genshin_impact(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Rainbow Six Siege',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Rainbow Six',
        emoji = "<:rainbow6:815421287206879253>"
    )
    async def rainbow_six_siege(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Apex Legends',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Apex Legends',
        emoji = "<:apexlegends:815419103278792714>"
    )
    async def apex_legends(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Fate/Grand Order',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Fate/Grand Order',
        emoji = "<:fgo:957039392910884924>"
    )
    async def fate_grand_order(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Valorant',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Valorant',
        emoji = "<:valorant:815419012636475403>"
    )
    async def valorant(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Dota 2',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dota 2',
        emoji = "<:dota:957043427172819014>"
    )
    async def dota_2(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'osu!',
        style = discord.ButtonStyle.blurple,
        custom_id = 'osu!',
        emoji = "<:osu:815540842986864640>"
    )
    async def osu(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Mobile Legend',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Mobile Legend',
        emoji = "<:ml:957043516343746580>"
    )
    async def mobile_legend(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)