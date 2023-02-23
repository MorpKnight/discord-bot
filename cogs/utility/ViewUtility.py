import discord
from discord.ui import View, Select
from discord.utils import get
from discord import SelectOption

class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def giveRole(self, interaction:discord.Interaction, custom_id):
        try:
            role = get(interaction.guild.roles, name=custom_id)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
        except:
            await interaction.response.send_message("Something went wrong", ephemeral=True)

class SingleRoleSelect(Select):
    def __init__(self, role_list, placeholder, custom_id):
        self.role_list = role_list
        super().__init__(
            placeholder=placeholder,
            options = [
                SelectOption(label=role, value=role) for role in self.role_list
            ],
            min_values=1,
            max_values=1,
            custom_id=custom_id
        )
    async def callback(self, interaction:discord.Interaction):
        try:
            selected_options = interaction.data['values']
            role = get(interaction.guild.roles, name=selected_options[0])
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have been assigned the role {role.name}", ephemeral=True)
        except:
            await interaction.response.send_message("Something went wrong", ephemeral=True)

class MultiRoleSelect(Select):
    def __init__(self, role_list, placeholder, max_values, custom_id):
        self.role_list = role_list
        super().__init__(
            placeholder=placeholder,
            options = [
                SelectOption(label=role, value=role) for role in self.role_list
            ],
            min_values=1,
            max_values=max_values,
            custom_id=custom_id
        )
    async def callback(self, interaction:discord.Interaction):
        try:
            selected_options = interaction.data['values']
            for role in selected_options:
                role = get(interaction.guild.roles, name=role)
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have been assigned the role {', '.join(selected_options)}", ephemeral=True)
        except:
            await interaction.response.send_message("Something went wrong", ephemeral=True)

class MultiRoleSelectEmoji(Select):
    def __init__(self, role_list, placeholder, max_values, emoji, custom_id):
        super().__init__(
            placeholder=placeholder,
            options = [
                SelectOption(label=role, value=role, emoji=emoji) for role, emoji in zip(role_list, emoji)
            ],
            min_values=1,
            max_values=max_values,
            custom_id=custom_id
        )
    async def callback(self, interaction:discord.Interaction):
        try:
            selected_options = interaction.data['values']
            for role in selected_options:
                role = get(interaction.guild.roles, name=role)
                await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have been assigned the role {', '.join(selected_options)}", ephemeral=True)
        except:
            await interaction.response.send_message("Something went wrong", ephemeral=True)