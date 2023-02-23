import discord
from discord.ext import commands


class onThread(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    
    @commands.command(name='solved')
    async def solved(self, ctx):
        assert isinstance(ctx.channel, discord.Thread)
        await ctx.message.add_reaction("✅")
        await ctx.channel.edit(locked=True, archived=True)
    
    @commands.Cog.listener()
    async def on_thread_create(self, thread:discord.Thread):
        if thread.parent_id == 1006373869302599780 or thread.parent_id == 1020007096181346324 or thread.parent_id == 1020107788761960539:
            return

        message = thread.get_partial_message(thread.id)
        try:
            await message.pin()
            await message.add_reaction("👌")
        except discord.HTTPException:
            pass

async def setup(client):
    await client.add_cog(onThread(client))