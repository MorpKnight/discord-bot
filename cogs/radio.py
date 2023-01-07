import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, app_commands
from discord.app_commands import Choice
import yaml

class discord_radio(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.voice_client = None
        self.voice_context = None
    
    async def radio_player(self, ctx:commands.Context, source:str):
        voiceChannel = ctx.author.voice
        if voiceChannel and voiceChannel.channel:
            if ctx.voice_client:
                pass
            else:
                await voiceChannel.channel.connect()
                self.voice_client = ctx.voice_client
                self.voice_context = ctx
                
            self.voice_client.play(FFmpegPCMAudio(source))
            await ctx.send("playing radio")
        
    @app_commands.command(name='radio', description='Play music from e-radio')
    @app_commands.choices(func=[
        Choice(name="add", value="add"),
        Choice(name="remove", value="remove"),
        Choice(name="list", value="list"),
        Choice(name="play", value="play"),
    ])
    @app_commands.choices(radio_name = [
        Choice(name="Prambors", value="Prambors"),
        Choice(name="Symphony 924", value="Symphony 924"),
        Choice(name="Japan Radio Osaka", value="Japan Radio Osaka"),
        Choice(name="NHK", value="NHK"),
        Choice(name="Japan A Radio", value="Japan A Radio"),
        Choice(name="J-Pop Powerplay Kawaii", value="J-Pop Powerplay Kawaii"),
    ])
    async def radio_music(self, interaction:discord.Interaction, func:Choice[str], radio_name:Choice[str]=None, new_name:str=None, new_url:str=None):
        if func.value == "add":
            with open("config.yml", "r") as f:
                config = yaml.safe_load(f)
            if radio_name.value in config["radio"]:
                await interaction.response.send_message("Radio already exists", ephemeral=True)
            else:
                config['radio'][f"{new_name}"] = f"{new_url}"
                with open("config.yml", "w") as f:
                    yaml.dump(config, f)
                await interaction.response.send_message("Radio added", ephemeral=True)
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
            await interaction.response.send_message(radio_list, ephemeral=True)
        elif func.value == "play":
            with open("config.yml", "r") as f:
                config = yaml.safe_load(f)
            if radio_name.value in config["radio"]:
                await self.radio_player(interaction, config["radio"][f"{radio_name.value}"])
            else:
                await interaction.response.send_message("Radio not found", ephemeral=True)

    # @commands.hybrid_group(name='radio', description='Play music from e-radio')
    # async def radio_music(self, ctx:commands.Context):
    #     if ctx.invoked_subcommand:
    #         await ctx.send(f"{ctx.prefix}help radio")
    
    # @radio_music.command(name='prambors', description='Play radio from PramborsFM')
    # async def radio_prambors(self, ctx:commands.Context):
    #     source = "https://22283.live.streamtheworld.com/PRAMBORS_FM.mp3?dist=pramborsweb&tdsdk=js-2.9&swm=false&pname=tdwidgets&pversion=2.9&banners=300x250&burst-time=15&sbmid=2602d526-9abc-43ce-ef30-98113d654ceb"
    #     await self.radio_player(ctx, source)

    # @radio_music.command(name="symphony924", description="Play radio from Symphony924")
    # async def radio_symphony(self, ctx:commands.Context):
    #     source = "https://14033.live.streamtheworld.com/SYMPHONY924AAC.aac?dist=radiosingapore"
    #     await self.radio_player(ctx, source)

    # @radio_music.command(name='japanimradio_osaka', description='Play radio from Japanimradio - Osaka')
    # async def radio_osaka(self, ctx:commands.Context):
    #     source = "https://ais-edge51-live365-dal02.cdnstream.com/a51684"
    #     await self.radio_player(ctx, source)
    
    # @radio_music.command(name='nhk', description='Plays NHK radio')
    # async def radio_nhk(self, ctx:commands.Context):
    #     source = "https://kathy.torontocast.com:3560/"
    #     await self.radio_player(ctx, source)
    
    # @radio_music.command(name='japan_a_radio', description='Plays Japan a Radio radio')
    # async def radio_japan_a(self, ctx:commands.Context):
    #     source = "https://audio.misproductions.com/japan128k"
    #     await self.radio_player(ctx, source)
    
    # @radio_music.command(name="powerplay_kawaii", description="Play J-Pop Powerplay Kawaii")
    # async def radio_jpop_kawaii(self, ctx:commands.Context):
    #     source = "https://kathy.torontocast.com:3060/;"
    #     await self.radio_player(ctx, source)

async def setup(client):
    await client.add_cog(discord_radio(client))