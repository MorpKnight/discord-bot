import asyncio
import functools
import os
import subprocess
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor

import discord
import yaml
from cogs.utility.voteButton import VoteButton
from cogs.utility.forceButton import ForceButton
from discord import app_commands
from discord.app_commands import Choice, checks
from discord.ext import commands, tasks
import datetime

class command_prompt_class():
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

class moderation(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.cmd = command_prompt_class()
        self.checkQuotaKick.start()
        self.checkQuotaBan.start()
    
    @tasks.loop(minutes=1)
    async def checkQuotaKick(self):
        with open("config.yml", "r+") as f:
            data = yaml.safe_load(f)
            now = datetime.datetime.now()
            if now.strftime("%H:%M:%S") == "00:00:00":
                data['quota']['kick'] = 5
                f.seek(0)
                yaml.dump(data, f, default_flow_style=False)
                f.truncate()
    
    @tasks.loop(hours=168)
    async def checkQuotaBan(self):
        with open("config.yml", "r+") as f:
            data = yaml.safe_load(f)
            now = datetime.datetime.now()
            if now.strftime("%H:%M:%S") == "00:00:00":
                data['quota']['ban'] = 2
                f.seek(0)
                yaml.dump(data, f, default_flow_style=False)
                f.truncate()

    @app_commands.command(name='move', description="Move member to another voice channel")
    @app_commands.checks.has_permissions(move_members=True)
    async def move(self, interaction:discord.Interaction, member:discord.Member, channel:discord.VoiceChannel):
        await member.move_to(channel)
        await interaction.response.send_message(f"{member.mention} has been moved to {channel.mention}", ephemeral=True)
    
    @app_commands.command(name='purge', description="Delete a number of messages from a channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_message(self, interaction:discord.Interaction, number:int):
        await interaction.channel.purge(limit=number)
        await interaction.response.send_message(f"{number} messages have been purged", ephemeral=True)

    @app_commands.command(name='command', description="Run command prompt/cmd")
    async def command_prompt(self, interaction:discord.Interaction, command:str):
        if not cmd:
            await interaction.response.send_message("Empty command")
        cmd = "".join(cmd[:])
        await interaction.response.send_message(f"Running `{cmd}`")
        loop = asyncio.get_event_loop()
        _, r_cmd = await loop.run_in_executor(ThreadPoolExecutor(), functools.partial(self.cmd.run_cmd, cmd))
        s_r_cmd = self.cmd.split_to_list(r_cmd, 1990)
        for m in s_r_cmd:
            await interaction.followup.send(f"```{m}```")
    
    @app_commands.command(name='reload', description='Reload an extension')
    @app_commands.choices(extension = [
        Choice(name=f"{f[:-3].capitalize()}", value=f"{f[:-3]}") for f in os.listdir("./cogs") if f.endswith(".py")
    ])
    async def re_load_extension(self, interaction:discord.Interaction, extension:Choice[str]):
        await self.client.reload_extension(f"cogs.{extension.value}")
        await interaction.response.send_message(f"Reloading {extension.value}")
    
    @app_commands.command(name = 'vote', description = "Vote to kick or ban a user")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.choices(type = [
        Choice(name = "Kick", value = "kick"),
        Choice(name = "Ban", value = "ban"),
        Choice(name = "Force Kick", value = "force_kick"),
        Choice(name = "Force Ban", value = "force_ban")
    ])
    async def vote_kick_ban(self, interaction:discord.Interaction, type:Choice[str], member:discord.Member, reason:str = None):
        if type.value == "kick":
            embed = discord.Embed(
                title = "Voting to KICK",
                description = f"{member.mention} has been put in voting to be kicked from the server.\nReason: {reason}",
                color = discord.Color.red()
            )
            embed.set_footer(text = f'Voting : 0/5')
            await interaction.response.send_message(embed=embed, view=VoteButton(member, type.value))
        elif type.value == "ban":
            embed = discord.Embed(
                title = "Voting to BAN",
                description = f"{member.mention} has been put in voting to be banned from the server.\nReason: {reason}",
                color = discord.Color.red()
            )
            embed.set_footer(text = f'Voting : 0/5')
            await interaction.response.send_message(embed=embed, view=VoteButton(member, type.value))
        elif type.value == "force_kick":
            embed = discord.Embed(
                title = "Voting to FORCE KICK",
                description = f"{member.mention} has been put in voting to be force kicked from the server.\nReason: {reason}",
                color = discord.Color.red()
            )   
            embed.set_footer(text = f'Voting : 0/5')
            await interaction.response.send_message(embed=embed, view=ForceButton(member, type.value))
        elif type.value == "force_ban":
            embed = discord.Embed(
                title = "Voting to FORCE BAN",
                description = f"{member.mention} has been put in voting to be force banned from the server.\nReason: {reason}",
                color = discord.Color.red()
            )
            embed.set_footer(text = f'Voting : 0/5')
            await interaction.response.send_message(embed=embed, view=ForceButton(member, type.value))
        else:
            await interaction.response.send_message("Invalid type", ephemeral=True)
    
    @commands.hybrid_command(name='unban', description = "Unban a user from the server")
    async def _unban(self, ctx, member:discord.Member, *, reason:str=None):
        await member.unban()
        await ctx.reply(f"{member.mention} has been unbanned from the server\nReason : {reason}", ephemeral = True)
    
    @app_commands.command(name='restore', description='Restore profile')
    async def restore_profile(self, interaction:discord.Interaction):
        await interaction.user.kick()
        await interaction.response.send_message(f"{interaction.user.mention} profile's restored", ephemeral=True)

async def setup(client):
    await client.add_cog(moderation(client))