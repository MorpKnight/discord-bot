from multiprocessing.connection import Client
import discord
from discord.ext import commands, tasks
from asyncio import sleep
import random
from discord import app_commands
from discord.app_commands import Choice
from discord_together import DiscordTogether

class command(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    
    @commands.hybrid_command(name='ping', description="Check bot's latency to server")
    async def _ping(self, ctx:commands.Context):
        result = round(self.client.latency * 1000)
        await ctx.reply(f"{result}ms")
    
    @commands.hybrid_command(name='whisper', description='Whisper someone')
    async def _whisper(self, ctx:commands.Context, member:discord.Member ,message:str):
        await member.send(message)
        await ctx.reply("Succeed sending message!", ephemeral=True)
    
    @app_commands.command(name='change_status', description="Change bot's status")
    @app_commands.choices(type=[
        Choice(name='playing', value='playing'),
        Choice(name='streaming', value='streaming'),
        Choice(name='listening', value='listening'),
        Choice(name='watching', value='watching')
    ])
    async def _change_status(self, interaction:discord.Interaction, type:Choice[str], name:str, url:str=None):
        if type == 'playing':
            await self.client.change_presence(activity=discord.Game(name=name))
        elif type == 'streaming':
            await self.client.change_presence(activity=discord.Streaming(name=name, url=url))
        elif type == 'listening':
            await self.client.change_presence(activity=discord.ActivityType.listening(name))
        elif type == 'watching':
            await self.client.change_presence(activity=discord.ActivityType.watching(name))
        
        await interaction.response.send_message(f"Changed status to {type} {name}")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.togetherControl = await DiscordTogether(self.client.http.token)
    
    @commands.hybrid_command(name='watch_youtube', description='Wathc youtube together using Discord')
    async def watchYoutube(self, ctx:commands.Context):
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, "youtube")
        embed = discord.Embed(
            title = 'Watch YouTube Together',
            description = f"[Click here]({link})",
            colour = discord.Colour.random()
        )

        embed.set_footer(text="At least 1 person need to click the hyperlink")
        await ctx.reply(embed=embed)
    
    @commands.hybrid_command(name='nuclearcode', description='Randomly select a doujinshi number')
    @commands.is_nsfw()
    async def _nuclearcode(self, ctx):
        result = random.randint(1, 440000)
        await ctx.reply(f'https://nhentai.net/g/{result}')
    
    @commands.hybrid_command(name='anonym', description="Send message anonymously to #anonym")
    @commands.dm_only()
    async def anonymous(self, ctx:commands.Context, *, message:str):
        anonymous_channel = self.client.get_channel(1011113637496242279)
        anonymous_log = self.client.get_channel(1011982504904900609)
        embed = discord.Embed(description=f"`{message}`")
        await ctx.send("Pesan terkirim", ephemeral=True)
        await anonymous_channel.send(embed=embed)
        await anonymous_log.send(f"`{message}` ~ {ctx.author}")
    
async def setup(client):
    await client.add_cog(command(client))