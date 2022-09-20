import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

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

    @commands.hybrid_group(name='radio', description='Play music from e-radio')
    async def radio_music(self, ctx:commands.Context):
        if ctx.invoked_subcommand:
            await ctx.send(f"{ctx.prefix}help radio")
    
    @radio_music.command(name='prambors', description='Play radio from PramborsFM')
    async def radio_prambors(self, ctx:commands.Context):
        source = "https://22283.live.streamtheworld.com/PRAMBORS_FM.mp3?dist=pramborsweb&tdsdk=js-2.9&swm=false&pname=tdwidgets&pversion=2.9&banners=300x250&burst-time=15&sbmid=2602d526-9abc-43ce-ef30-98113d654ceb"
        await self.radio_player(ctx, source)

    @radio_music.command(name="symphony924", description="Play radio from Symphony924")
    async def radio_symphony(self, ctx:commands.Context):
        source = "https://14033.live.streamtheworld.com/SYMPHONY924AAC.aac?dist=radiosingapore"
        await self.radio_player(ctx, source)

    @radio_music.command(name='japanimradio_osaka', description='Play radio from Japanimradio - Osaka')
    async def radio_osaka(self, ctx:commands.Context):
        source = "https://ais-edge51-live365-dal02.cdnstream.com/a51684"
        await self.radio_player(ctx, source)
    
    @radio_music.command(name='nkh', description='Plays NHK radio')
    async def radio_nhk(self, ctx:commands.Context):
        source = "https://kathy.torontocast.com:3560/"
        await self.radio_player(ctx, source)
    
    @radio_music.command(name='japan_a_radio', description='Plays Japan a Radio radio')
    async def radio_japan_a(self, ctx:commands.Context):
        source = "https://audio.misproductions.com/japan128k"
        await self.radio_player(ctx, source)

async def setup(client):
    await client.add_cog(discord_radio(client))