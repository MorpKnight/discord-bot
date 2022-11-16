import discord
from discord.utils import get
from discord.ui import View, button

class games(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
    
    @button(
        label = "Apex Legends",
        style = discord.ButtonStyle.blurple,
        custom_id= 'Apex Legends'
    )
    async def apex_legends(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @button(
        label = "VALORANT",
        style = discord.ButtonStyle.blurple,
        custom_id= 'VALORANT'
    )
    async def valorant(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @button(
        label = "Genshin Impact",
        style = discord.ButtonStyle.blurple,
        custom_id= 'Genshin Impact'
    )
    async def genshin_impact(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)

    @button(
        label = "Mobile Legends",
        style = discord.ButtonStyle.blurple,
        custom_id= 'Mobile Legends'
    )
    async def mobile_legends(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)

    @button(
        label = "osu!",
        style = discord.ButtonStyle.blurple,
        custom_id= 'osu!'
    )
    async def osu(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)

class kost(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
    
    @button(
        label = "Ya",
        style = discord.ButtonStyle.blurple,
        custom_id= 'Kost'
    )
    async def kost(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @button(
        label = "Ga",
        style = discord.ButtonStyle.blurple
    )
    async def gakost(self, interaction:discord.Interaction, button):
        await interaction.response.send_message("Kontol", ephemeral=True)