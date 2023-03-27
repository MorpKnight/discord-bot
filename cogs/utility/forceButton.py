import discord
from discord.ui import View
import yaml

class ForceButton(View):
    def __init__(self, member:discord.Member, type:str):
        super().__init__(timeout=15)
        self.member = member
        self.type = type
        self.voting = 0

    async def check_quota(self):
        with open('config.yml', 'r+') as f:
            config = yaml.safe_load(f)
            if config['quota'][f"{self.type}"] > 0:
                config['quota'][f"{self.type}"] -= 1
                f.seek(0)
                yaml.dump(config, f)
                f.truncate()
                return True
            else:
                return False
    
    async def onVoting(self, number, member, interaction:discord.Interaction):
        if number == 5:
            if not await self.check_quota():
                embed = discord.Embed(
                    title = "Error",
                    description = "You have reached the quota for kicking member.",
                    color = discord.Color.red()
                )
                await interaction.response.edit_message(embed=embed)
                return
            
            if self.type == 'kick':
                await member.kick()
                embed = discord.Embed(
                    title = "Kicked",
                    description = f"{member.mention} has been kicked from the server.",
                    color = discord.Color.red()
                )
            elif self.type == 'ban':
                await member.ban()
                embed = discord.Embed(
                    title = "Banned",
                    description = f"{member.mention} has been banned from the server.",
                    color = discord.Color.red()
                )
            for i in self.children:
                i.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed = discord.Embed(
                title = "Voting",
                description = f"{member.mention} has been put in voting to be {self.type} from the server.",
                color = discord.Color.red()
            )
            embed.set_footer(text = f'Voting : {self.voting}/5')
        try:
            await interaction.response.edit_message(embed=embed)
        except:
            pass
    
    @discord.ui.button(
        label = 'Yes',
        style = discord.ButtonStyle.red
    )
    async def ForceTrue(self, interaction, button):
        self.voting += 1
        await self.onVoting(self.voting, self.member, interaction)
        if self.voting != 5:
            try:
                await interaction.followup.send(f"{interaction.user} has voted to {self.type}.", ephemeral = True)
            except:
                pass
        else:
            pass