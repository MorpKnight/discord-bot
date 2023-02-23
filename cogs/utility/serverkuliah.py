import discord
from discord.ui import View, button, Select
from discord.utils import get
from discord import SelectOption

class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)

class games(RoleView):
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
    
    @button(
        label = 'GTA Online',
        style = discord.ButtonStyle.blurple,
        custom_id= 'GTA Online'
    )
    async def gta_online(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @button(
        label = 'The Forest',
        style = discord.ButtonStyle.blurple,
        custom_id= 'The Forest'
    )
    async def the_forest(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
class kost(RoleView):
    @button(
        label = "Ya",
        style = discord.ButtonStyle.blurple,
        custom_id= 'Kost'
    )
    async def kost(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @button(
        label = "Ga",
        style = discord.ButtonStyle.blurple,
        custom_id = 'GaKost'
    )
    async def gakost(self, interaction:discord.Interaction, button):
        await interaction.response.send_message("Kontol", ephemeral=True)

class comic(RoleView):
    @button(
        label = "(H)Anime",
        style = discord.ButtonStyle.blurple,
        custom_id = "(H)Anime"
    )
    async def hanime(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @button(
        label = "Manga",
        style = discord.ButtonStyle.blurple,
        custom_id = "Manga"
    )
    async def manga(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)
    
    @button(
        label = "Manhwa",
        style = discord.ButtonStyle.blurple,
        custom_id = "Manhwa"
    )
    async def manhwa(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)

    @button(
        label = "Doujin",
        style = discord.ButtonStyle.blurple,
        custom_id = "Doujin"
    )
    async def doujin(self, interaction, button):
        await self.giveRole(interaction, button.custom_id)

class addition_role_select(Select):
    def __init__(self, role_list, placeholder, custom_id):
        self.role_list = role_list
        super().__init__(
            placeholder=placeholder,
            options = [
                SelectOption(label=role, value=role) for role in self.role_list
            ],
            min_values=1,
            max_values=1,
            custom_id=custom_id
        )
    async def callback(self, interaction:discord.Interaction):
        selected_options = interaction.data['values']
        role = get(interaction.guild.roles, name=selected_options[0])
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)

class KelasMPKT(addition_role_select):
    def __init__(self):
        super().__init__(
            role_list=['MPKT 03', 'MPKT 04', 'MPKT 12', 'MPKT 21', 'MPKT 24', 'MPKT 29'],
            placeholder="Kelas MPKT",
            custom_id="kelas_mpkt"
        )
class KelasFismek(addition_role_select):
    def __init__(self):
        super().__init__(
            role_list=['Fismek 03', 'Fismek 06', 'Fismek 08', 'Fismek 13', 'Fismek 15'],
            placeholder='Kelas Fisika Mekanika',
            custom_id='kelas_fismek'
        )

class KelasAlin(addition_role_select):
    def __init__(self):
        super().__init__(
            role_list=['Aljabar Linear 05', 'Aljabar Linear 09', 'Aljabar Linear 13'],
            placeholder='Kelas Aljabar Linear',
            custom_id='kelas_alin'
        )

class Organisasi(addition_role_select):
    def __init__(self):
        super().__init__(
            role_list=['IME', 'EXERCISE'],
            placeholder="Organisasi",
            custom_id="organisasi"
        )

class alin(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasAlin())
    
class fismek(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasFismek())

class mpkt(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasMPKT())

class organisasi(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Organisasi())