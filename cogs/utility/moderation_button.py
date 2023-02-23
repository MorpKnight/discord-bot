import discord
from discord.ui import View


class kick_button(View):
    def __init__(self, member:discord.Member):
        super().__init__(timeout = 15)
        self.member = member
        self.voting = 0
    
    async def onVoting(self, number, member, interaction:discord.Interaction):
        if number == 5:
            await member.kick()
            embed = discord.Embed(
                title = "Kicked",
                description = f"{member.mention} has been kicked from the server.",
                color = discord.Color.red()
            )
            for i in self.children:
                i.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed = discord.Embed(
                title = "Voting",
                description = f"{member.mention} has been put in voting to be kicked from the server.",
                color = discord.Color.red()
            )
            embed.set_footer(text = f'Voting : {self.voting}/5')
        try:
            await interaction.response.edit_message(embed=embed)
        except:
            pass
    
    async def on_timeout(self):
        for i in self.children:
            i.disabled = True
    
    @discord.ui.button(
        label = 'Kick!',
        style = discord.ButtonStyle.red
    )
    async def kickTrue(self, interaction, button):
        self.voting += 1
        await self.onVoting(self.voting, self.member, interaction)
        if self.voting != 5:
            try:
                await interaction.followup.send(f"{interaction.user} has voted to kick.", ephemeral = True)
            except:
                pass
        else:
            pass
    
    @discord.ui.button(
        label = 'No',
        style = discord.ButtonStyle.green
    )
    async def kickFalse(self, interaction, button):
        self.voting -= 1
        if self.voting < 0:
            self.voting = 0
        await self.onVoting(self.voting, self.member, interaction)
        await interaction.followup.send(f"{interaction.user} has voted to not kick ", ephemeral = True)
    
    async def on_timeout(self, interaction:discord.Interaction):
        embed = discord.Embed(
            title = 'Timeout',
            description = "Voting has timed out.",
            color = discord.Color.red()
        )
        for i in self.children:
            i.disabled = True
        self.stop()
        await interaction.response.edit_message(embed=embed, view=self)



class ban_button(View):
    def __init__(self, member:discord.Member):
        super().__init__(timeout = 15)
        self.member = member
        self.voting = 0
    
    async def onVoting(self, number, member, interaction:discord.Interaction):
        if number == 5:
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
                description = f"{member.mention} has been put in voting to be banned from the server.",
                color = discord.Color.red()
            )
            embed.set_footer(text = f'Voting : {self.voting}/5')
        try:
            await interaction.response.edit_message(embed=embed)
        except:
            pass
    
    @discord.ui.button(
        label = 'Ban!',
        style = discord.ButtonStyle.red
    )
    async def banTrue(self, interaction, button):
        self.voting += 1
        await self.onVoting(self.voting, self.member, interaction)
        if self.voting != 5:
            try:
                await interaction.followup.send(f"{interaction.user} has voted to ban.", ephemeral = True)
            except:
                pass
        else:
            pass
    
    @discord.ui.button(
        label = 'No',
        style = discord.ButtonStyle.green
    )
    async def banFalse(self, interaction, button):
        self.voting -= 1
        if self.voting < 0:
            self.voting = 0
        await self.onVoting(self.voting, self.member, interaction)
        await interaction.followup.send(f"{interaction.user} has voted to not ban ", ephemeral = True)
    
    async def on_timeout(self, interaction:discord.Interaction):
        embed = discord.Embed(
            title = 'Timeout',
            description = "Voting has timed out.",
            color = discord.Color.red()
        )
        for i in self.children:
            i.disabled = True
        self.stop()
        await interaction.response.edit_message(embed=embed, view=self)