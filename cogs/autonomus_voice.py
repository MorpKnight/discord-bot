from asyncio import sleep

import discord
from discord import app_commands
from discord.ext import commands, tasks


class autonomus_vc(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.channel = []
        self.information_channel_id = None
        self.check_channel.start()

    @app_commands.command(name='create_vc', description="Create voice channel temporart")
    async def create_voice(self, interaction:discord.Interaction, category_id:int ,channel_name:str):
        category = discord.utils.get(interaction.guild.categories, id=category_id)
        await interaction.guild.create_voice_channel(name=channel_name, category=category)
        fetchVoice = discord.utils.get(interaction.guild.channels, name=channel_name)
        await interaction.response.send_message(f"Successfully created {fetchVoice.mention}")
        self.information_channel_id = interaction.channel.id
    
    @tasks.loop(seconds=60)
    async def check_channel(self):
        for guild in self.client.guilds:
            for channel in guild.voice_channels:
                if channel.name in self.channel:
                    if channel.members == []:
                        message_channel = self.client.get_channel(self.information_channel_id)
                    message = await message_channel.send(f"Temporary voice channel will be deleted in 5s")
                    await sleep(5)
                    try:
                        self.channel.pop(self.channel.index(channel.name))
                        self.information_channel_id = None
                        await channel.delete()
                        await message.delete()
                    except:
                        pass
                else:
                    pass

async def setup(client):
    await client.add_cog(autonomus_vc(client))