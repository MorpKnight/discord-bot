import asyncio
import functools
import os
import random
import subprocess
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.connection import Client

import aiohttp
import discord
import dotenv
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
from discord_together import DiscordTogether

dotenv.load_dotenv()

class command(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    
    def run_cmd(cmd):
        print(f"Init run cmd: `{cmd}`")
        try:
            cmd_list = cmd.split(" ")
            run = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            run_err = run.stderr.decode('utf-8')
            if run_err != "":
                return False, run_err
            return True, run.stdout.decode('utf-8')
        except Exception as err:
            return False, str(err)

    def split_to_list(text: str, max_len: int = 1000):
        spllited_text = []
        if len(text) >= max_len:
            remain_text = text
            while True:
                split_by_new_line = remain_text.split("\n")
                app_text = ""
                for new_line_text in split_by_new_line:
                    new_line_text = new_line_text + "\n"
                    if len(app_text) + len(new_line_text) >= max_len:
                        break
                    app_text += new_line_text

                spllited_text.append(app_text)
                remain_text = remain_text[len(app_text):]

                if remain_text == "":
                    break
        else:
            spllited_text = [text]
        return spllited_text

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
    
    @commands.command(name='cmd')
    @commands.is_owner()
    async def _cmd(self, ctx, *, cmd):
        if not cmd:
            await ctx.send("Empty command")
        cmd = "".join(cmd[:])
        await ctx.send(f"Running `{cmd}`")
        loop = asyncio.get_event_loop()
        _, r_cmd = await loop.run_in_executor(ThreadPoolExecutor(), functools.partial(command.run_cmd, cmd))
        s_r_cmd = command.split_to_list(r_cmd, 1990)
        for m in s_r_cmd:
            await ctx.send(f"```{m}```")
        
    @app_commands.command(name='testattachment', description='Test attachment')
    async def _testattachment(self, interaction:discord.Interaction, attachment:discord.Attachment):
        await interaction.response.send_message(f"Attachment: {attachment.url}")
    
    @app_commands.command(name='askgpt', description="Ask GPT-3")
    @app_commands.describe(creativity="Creativity of GPT-3 0 - 1.0 (float)", question="Question to ask GPT-3 (str)")
    async def _askgpt(self, interaction:discord.Interaction, creativity:float, question:str):
        if creativity > 1.0:
            creativity = 1.0
        elif creativity < 0:
            creativity = 0.0
        
        await interaction.response.defer()

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    payload = {
                        "model": "text-davinci-003",
                        "prompt": question,
                        "max_tokens": 2048,
                        "temperature": creativity,
                    }

                    headers = {
                        "Authorization": "Bearer " + os.getenv("GPT3_TOKEN"),
                    }
                    async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
                        data = await resp.json()
                        resp = f"""Question: 
{question}
Answer: 
```{data['choices'][0]['text']}```"""
                        embed = discord.Embed(
                            title = "GPT-3",
                            description = resp,
                            colour = discord.Colour.random()
                        )
                        embed.set_footer(text="Powered by OpenAI")
                        await interaction.followup.send(embed=embed)
                        break
            except discord.errors.NotFound:
                await sleep(1)

async def setup(client):
    await client.add_cog(command(client))