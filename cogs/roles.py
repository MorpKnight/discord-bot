import discord
from discord.ext import commands
from discord.utils import get
from cogs.utility.serverkuliah import *
from asyncio import sleep

class adding_role(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    
    @commands.hybrid_command(name="roles")
    async def put_roles(self, ctx:commands.Context):
        await ctx.message.delete()
        await ctx.send("Pilih role game mu nak", view=games_pribadi())
        await sleep(2)
        await ctx.send("Kau ngekost kah?", view=kost())
        await sleep(2)
        await ctx.send("Wibu macam mana kau?", view=comic())

async def setup(client):
    await client.add_cog(adding_role(client))