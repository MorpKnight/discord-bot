import discord
from discord.ui import View
from discord.utils import get


class games(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"Role {role.name} telah anda ambil", ephemeral=True)
    
    @discord.ui.button(
        label = "Apex Legends",
        style= discord.ButtonStyle.blurple,
        custom_id="Apex Legends",
        emoji="<:apexlegends:1001616780860596305>"
    )
    async def apex_legends(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Genshin Impact',
        style=discord.ButtonStyle.blurple,
        custom_id="Genshin Impact",
        emoji="<:genshinimpact:1001616581723422794>"
    )
    async def genshin_impact(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @discord.ui.button(
        label = "Valorant",
        style=discord.ButtonStyle.blurple,
        custom_id="Valorant",
        emoji = '<:valorant:1001616587335422053>'
    )
    async def valorant(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @discord.ui.button(
        label = 'Minecraft',
        style=discord.ButtonStyle.blurple,
        custom_id="Minecraft",
        emoji='<:minecraft:1001616577680125982>'
    )
    async def minecraft(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @discord.ui.button(
        label = 'Fate/Grand Order',
        style=discord.ButtonStyle.blurple,
        custom_id="Fate/Grand Order",
        emoji='<:fategrandorder:1001616585397649428>'
    )
    async def fate_go(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @discord.ui.button(
        label = 'osu!',
        style=discord.ButtonStyle.blurple,
        custom_id="osu!",
        emoji='<:osu:1001616579852783716>'
    )
    async def osu(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @discord.ui.button(
        label = 'Stumble',
        style=discord.ButtonStyle.blurple,
        custom_id= "Stumble",
        emoji = '<:stumble:1001616573271908412>'
    )
    async def stumble(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @discord.ui.button(
        label = 'Mobile Legends',
        style=discord.ButtonStyle.blurple,
        custom_id="Mobile Legends",
        emoji='<:mobilelegends:1001616571342540901>'
    )
    async def mobile_legends(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @discord.ui.button(
        label = 'The Forest',
        style=discord.ButtonStyle.blurple,
        custom_id="The Forest",
        emoji="<:theforest:1066992765591887972>"
    )
    async def theforest(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)

class kost(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"Role {role.name} telah anda ambil", ephemeral=True)

    @discord.ui.button(
        label = 'Yes',
        style = discord.ButtonStyle.success,
        custom_id = "Kost",
        emoji = "🏠"
    )
    async def ngekost(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @discord.ui.button(
        label = 'Pulang Pergi / PP',
        style = discord.ButtonStyle.danger,
        custom_id = "Pulang Pergi",
        emoji = "🚶"
    )
    async def pulang_pergi(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)