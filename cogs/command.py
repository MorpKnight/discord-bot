import asyncio
import functools
import os
import random
import subprocess
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import discord
import dotenv
import google.generativeai as palm
import openai
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord_together import DiscordTogether

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')
palm.configure(api_key=os.getenv('GOOGLE_KEY'))

class command(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.chatHistory = []
    
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
    
    def ask_gpt4(question, conversation_history):
        conversation_history.append(f'User: {question}\n')
        prompt = ''.join(conversation_history)

        response = openai.Completion.create(
            engine="text-davinci-003",
            max_tokens=2048,
            prompt=prompt,
        )

        answer = response.choices[0].text.strip()
        conversation_history.append(f'AI: {answer}\n')

        return answer
    
    def code_gpt4(question, code):
        prompt = f'{question}\n```{code}```\n'

        response = openai.Completion.create(
            engine="text-davinci-003",
            max_tokens=2048,
            prompt=prompt
        )

        answer = response.choices[0].text.strip()
        return answer

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
        result = random.randint(1, 500000)
        await ctx.reply(f'https://nhentai.net/g/{result}')
    
    @commands.hybrid_command(name='anonym', description="Send message anonymously to #anonym")
    @commands.dm_only()
    async def anonymous(self, ctx:commands.Context, *, message:str):
        anonymous_channel = self.client.get_channel(1011113637496242279)
        anonymous_log = self.client.get_channel(1011982504904900609)
        embed = discord.Embed(description=f"`{message}`")
        await ctx.send("Pesan terkirim", ephemeral=True)
        await anonymous_channel.send(embed=embed)
        await anonymous_log.send(f"`{message}` ~ {ctx.author.global_name}")
    
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

    @app_commands.command(name='bard', description="Ask bard about something (english only)")
    async def _askBard(self, interaction:discord.Interaction, question:str, temperature:float=0.5):
        await interaction.response.defer()
        self.chatHistory.append(question)
        response = palm.chat(messages=self.chatHistory, temperature=temperature)
        await interaction.followup.send(f"{response.last}")
        
    # @app_commands.command(name='askgpt', description="Ask ChatGPT-")
    # async def _askgpt(self, interaction:discord.Interaction, question:str):

    #     await interaction.response.defer()
    #     response = command.ask_gpt4(question, self.conversation_history)

    #     if response[:3] == "AI:":
    #         response = response[3:]

    #     embed = discord.Embed(
    #         title = 'AskGPT',
    #         description=f"**Question**: {question}\n**Answer:**\n```{response}```",
    #         colour = discord.Colour.random()
    #     )

    #     await interaction.followup.send(embed=embed)

    # @app_commands.command(name='codegpt', description="Code with GPT")
    # async def _codegpt(self, interaction:discord.Interaction, file:discord.Attachment, args:str="Fix this code"):
    #     await interaction.response.defer()
    #     await file.save(f'./{file.filename}')

    #     with open(f'./{file.filename}', 'r') as f:
    #         code = f.read()
        
    #     extension = file.filename.split('.')[-1]

    #     response = command.code_gpt4(args, code)

    #     embed = discord.Embed(
    #         title = 'CodeGPT',
    #         description=f"**Args**: {args}\n**Code:**\n```{extension}\n{code}```\n**Output:**\n```{extension}\n{response}```",
    #         colour = discord.Colour.random()
    #     )

    #     await interaction.followup.send(embed=embed)
        
    #     os.remove(f'./{file.filename}')

async def setup(client):
    await client.add_cog(command(client))