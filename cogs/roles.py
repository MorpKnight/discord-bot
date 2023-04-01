import discord
from discord import app_commands
from discord.app_commands import Choice, choices
from discord.ext import commands

import cogs.utility.ftui_roles as RolesFTUI
import cogs.utility.serverkuliah as RolesBackroom
import cogs.utility.serversma as RolesSMA
import cogs.utility.tekkomp_roles as RolesTekkom

role_list = ['games', 'kost', 'comic', 'departemen', 'prodi', 'animeenjoyer', 'alin', 'fismek', 'mpkt', 'proglan', 'oak', 'organisasi']
class adding_role(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    
    @app_commands.command(name="roles", description="Show roles")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.choices(option = [
        Choice(name='Display message', value='display'),
        Choice(name='Edit message', value='edit'),
    ])
    @app_commands.choices(filename = [
        Choice(name="FTUI", value="ftui"),
        Choice(name="SMA", value="sma"),
        Choice(name="Tekkom", value="tekkom"),
        Choice(name="Backroom", value="backroom")
    ])
    @app_commands.choices(classname = [
        Choice(name=role, value=role) for role in role_list
    ])
    async def showroles(self, interaction:discord.Interaction, channel:discord.TextChannel ,option:Choice[str], filename:Choice[str], classname:Choice[str], arg:str=None, msgid:str=None):
        if option.value == 'display':
            try:
                match filename.value:
                    case 'ftui':
                        match classname.value:
                            case 'games':
                                viewRole = RolesFTUI.games()
                            case 'departemen':
                                viewRole = RolesFTUI.departemen()
                            case 'prodi':
                                viewRole = RolesFTUI.prodi()
                            case 'animeenjoyer':
                                viewRole = RolesFTUI.animeenjoyer()
                    case 'sma':
                        viewRole = RolesSMA.games()
                    case 'tekkom':
                        match classname.value:
                            case 'kost':
                                viewRole = RolesTekkom.kost()
                            case 'games':
                                viewRole = RolesTekkom.games()
                    case 'backroom':
                        match classname.value:
                            case 'comic':
                                viewRole = RolesBackroom.comic()
                            case 'alin':
                                viewRole = RolesBackroom.alin()
                            case 'fismek':
                                viewRole = RolesBackroom.fismek()
                            case 'mpkt':
                                viewRole = RolesBackroom.mpkt()
                            case 'proglan':
                                viewRole = RolesBackroom.proglan()
                            case 'oak':
                                viewRole = RolesBackroom.oak()
                            case 'organisasi':
                                viewRole = RolesBackroom.organisasi()
                            case 'games':
                                viewRole = RolesBackroom.games()
                            case 'kost':
                                viewRole = RolesBackroom.kost()
                        
                await channel.send(content=arg, view=viewRole)
                await interaction.response.send_message(content="Message sent", ephemeral=True)
            except:
                await interaction.response.send_message(content="Error", ephemeral=True)

        elif option.value == 'edit':
            try:
                message = await channel.fetch_message(msgid)
                await message.edit(content=arg)
                await interaction.response.send_message(content="Message edited", ephemeral=True)
            except:
                await interaction.response.send_message(content="Error", ephemeral=True)
    
    @app_commands.command(name="setup_roles", description="Setup server roles")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.choices(filename=[
        Choice(name="FTUI", value="ftui"),
        Choice(name="SMA", value="sma"),
        Choice(name="Tekkom", value="tekkom"),
        Choice(name="Backroom", value="backroom")
    ])
    async def setup_roles(self, interaction: discord.Interaction, channel: discord.TextChannel, filename: Choice[str]):
        if filename.value == 'ftui':
            views = [RolesFTUI.games(), RolesFTUI.departemen(), RolesFTUI.prodi(), RolesFTUI.animeenjoyer()]
        elif filename.value == 'sma':
            views = [RolesSMA.games()]
        elif filename.value == 'tekkom':
            views = [RolesTekkom.kost(), RolesTekkom.games()]
        elif filename.value == 'backroom':
            views = [
                RolesBackroom.games(),
                RolesBackroom.kost(),
                RolesBackroom.comic(),
                RolesBackroom.organisasi(),
                RolesBackroom.alin(),
                RolesBackroom.fismek(),
                RolesBackroom.mpkt(),
                RolesBackroom.proglan(),
                RolesBackroom.oak()
            ]

        for view in views:
            await channel.send(view=view)


async def setup(client):
    await client.add_cog(adding_role(client))