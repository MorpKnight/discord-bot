from asyncio import sleep

import discord
from discord import app_commands
from discord.app_commands import Choice, choices
from discord.ext import commands
from discord.ext.commands import group, hybrid_command, hybrid_group
from discord.utils import get


class broadcast(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        
    @app_commands.command(name='broadcast', description="Broadcast a message/embed")
    @app_commands.choices(type = [
        Choice(name="Message", value="message"),
        Choice(name="Embed", value="embed")
    ])
    @app_commands.choices(receivers = [
        Choice(name="Channel", value="channel"),
        Choice(name="Role", value="role"),
        Choice(name="User", value="user"),
        Choice(name="All", value="all"),
        Choice(name="All Except", value="except")
    ])
    async def _broadcast(self, interaction:discord.Interaction, 
        type:Choice[str], receivers:Choice[str], 
        message:str, channel:discord.TextChannel = None, 
        role:discord.Role = None, member:discord.Member = None,
        title:str = None, color:str = None, footer:str = None,
        image:discord.Attachment = None, thumbnail:discord.Attachment = None,
        intro:str = None):
        if type.value == 'message':
            message = message.split('  ')
            newMessage = ''
            for i in message:
                newMessage += f"{i}\n"
            match receivers.value:
                case 'channel':
                    await channel.send(newMessage)
                case 'role':
                    for i in role.members:
                        await sleep(2)
                        await i.send(newMessage)
                case 'user':
                    await member.send(newMessage)
                case 'all':
                    for i in interaction.guild.members:
                        await sleep(2)
                        await i.send(newMessage)
                case 'except':
                    for i in interaction.guild.members:
                        if i not in role.members:
                            await sleep(2)
                            await i.send(newMessage)
        elif type.value == 'embed':
            embed = discord.Embed(title = title, color = color, footer = footer)
            if image:
                embed.set_image(url = image.url)
            if thumbnail:
                embed.set_thumbnail(url = thumbnail.url)
            if intro:
                embed.description = intro
            match receivers.value:
                case 'channel':
                    await channel.send(embed = embed)
                case 'role':
                    for i in role.members:
                        await sleep(2)
                        await i.send(embed = embed)
                case 'user':
                    await member.send(embed = embed)
                case 'all':
                    for i in interaction.guild.members:
                        await sleep(2)
                        await i.send(embed = embed)
                case 'except':
                    for i in interaction.guild.members:
                        if i not in role.members:
                            await sleep(2)
                            await i.send(embed = embed)
            
        await interaction.response.send_message(f"Message sent to {receivers.value}", ephemeral = True)

async def setup(client):
    await client.add_cog(broadcast(client))