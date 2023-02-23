import discord
from discord.ext import commands


class handler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.reply("You are not the bot owner")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"{error}. Please check your command")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have permission to use this command")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply("Command on cooldown")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Missing argument, please check your command")
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply("You don't have permission to use this command")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Command on invoke error")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You had no perms to run this command")

async def setup(client):
    await client.add_cog(handler(client))