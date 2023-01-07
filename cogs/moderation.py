import asyncio
import functools
import subprocess
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor
from cogs.utility.serverkuliah import games_pribadi, kost
from cogs.utility.moderation_button import kick_button, ban_button
import discord
from discord import app_commands
from discord.app_commands import Choice, checks
from discord.ext import commands
import os

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
        # Choice(name="anime", value="anime"),
        # Choice(name='autonomus_voice', value='autonomus_voice'),
        # Choice(name='broadcast_message', value='broadcast_message'),
        # Choice(name='command', value='command'),
        # Choice(name='errorhandler', value='errorhandler'),
        # Choice(name='member_join', value='member_join'),
        # Choice(name='message', value='message'),
        # Choice(name='moderation', value='moderation'),
        # Choice(name='radio', value='radio'),
        # Choice(name='voicechannel', value='voicechannel'),

    ])
    async def re_load_extension(self, interaction:discord.Interaction, extension:Choice[str]):
        await self.client.reload_extension(f"cogs.{extension.value}")
        await interaction.response.send_message(f"Reloading {extension.value}")

    @commands.hybrid_command(name='kick', description = "Kick a user from the server")
    @commands.has_permissions(kick_members = True)
    async def _kick(self, ctx, member:discord.Member, *, reason:str = None):
        embed = discord.Embed(
            title = "Voting to KICK",
            description = f"{member.mention} has been put in voting to be kicked from the server.\nReason: {reason}",
            color = discord.Color.red()
        )
        embed.set_footer(text = f'Voting : 0/5')
        await ctx.send(embed=embed, view=kick_button(member))
    
    @commands.hybrid_command(name='ban', description = "Ban a user from the server")
    @commands.has_permissions(ban_members = True)
    async def _ban(self, ctx, member:discord.Member, *, reason:str = None):
        embed = discord.Embed(
            title = "Voting to BAN",
            description = f"{member.mention} has been put in voting to be banned from the server.\nReason: {reason}",
            color = discord.Color.red()
        )
        embed.set_footer(text = 'Voting : 0/5')
        await ctx.send(embed=embed, view=ban_button(member))
    
    @commands.hybrid_command(name='unban', description = "Unban a user from the server")
    async def _unban(self, ctx, member:discord.Member, *, reason:str=None):
        await member.unban()
        await ctx.reply(f"{member.mention} has been unbanned from the server\nReason : {reason}", ephemeral = True)
    
    # @commands.hybrid_command(name='poll', description="Polling warga")
    # async def polling_warga(self, ctx:commands.Context, judul:str, timeout:int):
    #     await ctx.send(f"Polling {judul} has been created")
    #     await ctx.send(f"Polling {judul} has been created", view=polling_warga(judul, timeout)) 

async def setup(client):
    await client.add_cog(moderation(client))