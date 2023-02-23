import discord
import yaml
from discord import FFmpegPCMAudio, app_commands
from discord.app_commands import Choice
from discord.ext import commands


class discord_radio(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.voice_client = None
        self.voice_context = None
    
    async def radio_player(self, interaction:discord.Interaction, source:str):
        voiceChannel = interaction.user.voice
        if voiceChannel and voiceChannel.channel:
            if interaction.guild.voice_client:
                pass
            else:
                await voiceChannel.channel.connect()
                self.voice_client = interaction.guild.voice_client
                self.voice_context = interaction
                
            self.voice_client.play(FFmpegPCMAudio(source))
            await interaction.response.send_message("Playing radio", ephemeral=True)
        
    @app_commands.command(name='radio', description='Play music from e-radio')
    @app_commands.choices(func=[
        Choice(name="Add", value="add"),
        Choice(name="Remove", value="remove"),
        Choice(name="List", value="list"),
        Choice(name="Play", value="play"),
        Choice(name='Stop', value='stop')
    ])
    @app_commands.choices(radio_name = [
        Choice(name=f"{key}", value=f"{key}") for key, value in yaml.safe_load(open("config.yml", "r"))["radio"].items()
    ])
    async def radio_music(self, interaction:discord.Interaction, func:Choice[str], radio_name:Choice[str]=None, new_name:str=None, new_url:str=None):
        if func.value == "add":
            with open("config.yml", "r") as f:
                config = yaml.safe_load(f)
            if radio_name.value in config["radio"]:
                await interaction.response.send_message("Radio already exists")
            else:
                config['radio'][f"{new_name}"] = f"{new_url}"
                with open("config.yml", "w") as f:
                    yaml.dump(config, f)
                await interaction.response.send_message("Radio added")
        elif func.value == "remove":
            with open("config.yml", "r") as f:
                config = yaml.safe_load(f)
            if radio_name in config["radio"]:
                del config["radio"][f"{radio_name.value}"]
                with open("config.yml", "w") as f:
                    yaml.dump(config, f)
                await interaction.response.send_message("Radio removed")
            else:
                await interaction.response.send_message("Radio not found")
        elif func.value == "list":
            with open("config.yml", "r") as f:
                config = yaml.safe_load(f)
            radio_list = ""
            for key, value in config["radio"].items():
                radio_list += f"{key}\n"
            await interaction.response.send_message(radio_list)
        elif func.value == "play":
            with open("config.yml", "r") as f:
                config = yaml.safe_load(f)
            if radio_name.value in config["radio"]:
                await self.radio_player(interaction, config["radio"][f"{radio_name.value}"])
            else:
                await interaction.response.send_message("Radio not found")
        elif func.value == "stop":
            if interaction.guild.voice_client:
                self.voice_client = None
                self.voice_context = None
                interaction.guild.voice_client.disconnect()
                await interaction.response.send_message("Stopped")
            else:
                await interaction.response.send_message("Not playing")


async def setup(client):
    await client.add_cog(discord_radio(client))