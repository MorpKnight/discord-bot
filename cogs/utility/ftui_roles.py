import discord
from discord.ui import View, button
from discord.utils import get

class games(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
    
    @button(
        label = 'Valorant',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Valorant',
        emoji = '<:valorant:979988251215536179>'
    )
    async def valorant(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Apex Legends',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Apex Legends',
        emoji = "<:apex:979987898071916565>"
    )
    async def apex_legends(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'CS:GO',
        style = discord.ButtonStyle.blurple,
        custom_id = 'CS:GO',
        emoji = "<:csgo:979988255284002886>"
    )
    async def cs_go(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Genshin Impact',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Genshin Impact',
        emoji = "<:genshin:979988252905832468>"
    )
    async def genshin_impact(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Rainbow Six Siege',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Rainbow Six Siege',
        emoji = "<:rainbowsix:979989238357557278>"
    )
    async def rainbow_six_siege(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Minecraft',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Minecraft',
        emoji='<:minecraft:979988672638226462>'
    )
    async def minecraft(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'PUBG PC',
        style = discord.ButtonStyle.blurple,
        custom_id = 'PUBG PC',
        emoji = '<:pubgpc:979988669970657330>'
    )
    async def pubg_pc(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'PUBG Mobile',
        style = discord.ButtonStyle.blurple,
        custom_id = 'PUBGM',
        emoji='<:pubgm:979988670721450014>'
    )
    async def pubg_mobile(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Fate/Grand Order',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Fate/Grand Order',
        emoji = '<:fgo:980603043324256256>'
    )
    async def fate_grand_order(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Dota 2',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dota 2',
        emoji="<:dota:986615940261232660>"
    )
    async def dota_2(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'osu!',
        style = discord.ButtonStyle.blurple,
        custom_id = 'osu!',
        emoji='<:osu:986616086210437160>'
    )
    async def osu(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

class departemen(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
    
    @button(
        label = 'Dept. Teknik Sipil dan Lingkungan',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dept. Teknik Sipil dan Lingkungan',
        emoji = "🔨"
    )
    async def teknik_sipil_dan_lingkungan(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Dept. Teknik Mesin',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dept. Teknik Mesin',
        emoji = "⚙️"
    )
    async def teknik_mesin(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Dept. Teknik Elektro',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dept. Teknik Elektro',
        emoji="⚡"
    )
    async def teknik_elektro(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Dept. Teknik Metalurgi dan Material',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dept. Teknik Metalurgi dan Material',
        emoji="🧱"
    )
    async def teknik_metalurgi_dan_material(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Dept. Teknik Arsitektur',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dept. Teknik Arsitektur',
        emoji = "🏠"
    )
    async def teknik_arsitektur(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Dept. Teknik Kimia',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dept. Teknik Kimia',
        emoji = "🧪"
    )
    async def teknik_kimia(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Dept. Teknik Industri',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Dept. Teknik Industri',
        emoji = '🏭'
    )
    async def teknik_industri(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

class prodi(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
    
    @button(
        label = 'Teknik Sipil',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Teknik Sipil',
        emoji = "👷"
    )
    async def teknik_sipil(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = "Teknik Lingkungan",
        style = discord.ButtonStyle.blurple,
        custom_id = "Teknik Lingkungan",
        emoji = '🍀'
    )
    async def teknik_lingkungan(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Teknik Mesin',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Teknik Mesin',
        emoji = "⚙️"
    )
    async def teknik_mesin(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Teknik Perkapalan',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Teknik Perkapalan',
        emoji = "🛳"
    )
    async def teknik_perkapalan(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = "Teknik Elektro",
        style = discord.ButtonStyle.blurple,
        custom_id = "Teknik Elektro",
        emoji = "⚡"
    )
    async def teknik_elektro(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = "Teknik Komputer",
        style = discord.ButtonStyle.blurple,
        custom_id = "Teknik Komputer",
        emoji = "💻"
    )
    async def teknik_komputer(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = "Teknik Biomedik",
        style = discord.ButtonStyle.blurple,
        custom_id = "Teknik Biomedik",
        emoji = "🧬"
    )
    async def teknik_biomedik(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Teknik Metalurgi dan Material',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Teknik Metalurgi dan Material',
        emoji = "🧱"
    )
    async def teknik_metalurgi_dan_material(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Arsitektur',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Arsitektur',
        emoji = "🏠"
    )
    async def arsitektur(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = 'Arsitektur Interios',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Arsitektur Interior',
        emoji = "🛋️"
    )
    async def arsitektur_interios(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

    @button(
        label = "Teknik Kimia",
        style = discord.ButtonStyle.blurple,
        custom_id = "Teknik Kimia",
        emoji = "🧪"
    )
    async def teknik_kimia(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Teknik Bioproses',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Teknik Bioproses',
        emoji = "🧫"
    )
    async def teknik_bioproses(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)
    
    @button(
        label = 'Teknik Industri',
        style = discord.ButtonStyle.blurple,
        custom_id = 'Teknik Industri',
        emoji = '🏭'
    )
    async def teknik_industri(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)

class animeenjoyer(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        role = get(interaction.guild.roles, name=custom_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
    
    @discord.ui.button(
        label = "Nimek Enjoyer",
        style = discord.ButtonStyle.blurple,
        custom_id = "Nimek Enjoyer",
    )
    async def nimek_enjoyer(self, interaction, button):
        await self.giveRole(interaction=interaction, custom_id=button.custom_id)