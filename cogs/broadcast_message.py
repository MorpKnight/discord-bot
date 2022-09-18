import discord
from discord.ext import commands
from discord.ext.commands import hybrid_command, hybrid_group, group
from asyncio import sleep

class broadcast(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    
    async def send_broadcast(self, ctx,  message, receivers):
        splitMessage = message.split('  ')
        newMessage = ''
        for i in splitMessage:
            newMessage += f"{i}\n"
        await receivers.send(newMessage)
        await ctx.send(f"Message sent to {receivers.mention}", ephemeral = True)
    
    async def send_broadcasts(self, ctx, message, receivers):
        for i in receivers.members:
            await self.send_broadcast(ctx, message, i)
            await sleep(2)
        await ctx.send(f"Message sent to {receivers.mention}", ephemeral = True, delete_after = 1)

    @commands.hybrid_group(name='broadcast', description='Broadcast a message')
    async def broadcast(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.prefix}help broadcast")\
    
    @broadcast.command(name='channel', description='Broadcast a message to a channel')
    async def bcchannel(self, ctx, channel:discord.TextChannel, *, message:str):
        await self.send_broadcast(ctx, message, channel)
        await ctx.send(f"Message sent to {channel.mention}", ephemeral=True)
    
    @broadcast.command(name='role', description='Broadcast a message to a role')
    async def bcrole(self, ctx, role:discord.Role, *, message:str):
        await self.send_broadcasts(ctx, message, role)
        await ctx.send(f"Message sent to {role}", ephemeral=True)
    
    @broadcast.command(name='user', description='Broadcast a message to a user')
    async def bcuser(self, ctx, user:discord.User, *, message:str):
        await self.send_broadcast(ctx, message, user)
        await ctx.send(f"Message sent to {user}", ephemeral=True)
    
    @broadcast.command(name='all', description='Broadcast a message to all')
    async def bcall(self, ctx, message:str):
        server = ctx.guild
        await self.send_broadcasts(ctx, message, server)
        await ctx.send(f"Message sent to all", ephemeral=True)
    
    @broadcast.command(name='except', description='Broadcast a message to all except a role')
    async def bcexcept(self, ctx, role:discord.Role, *, message:str):
        for i in ctx.guild.members:
            if i not in role.members:
                await self.send_broadcast(ctx, message, i)
                await sleep(2)
        await ctx.send(f"Message sent to all except {role}", ephemeral=True)

    @commands.hybrid_group(name='embed', description='Broadcast a message with embed')
    async def embed(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.prefix}help embed")
    
    @embed.command(name='channel', description='Broadcast a message with embed to a channel. To break row use double space. Color using hex format')
    async def embedchannel(self, ctx, channel:discord.TextChannel, title:str, message:str, color:str=None, footer:str=None, image:str=None,thumbnail:str=None, intro:str=None):
        splitMessage = message.split('  ')
        newMessage = ''
        for i in splitMessage:
            newMessage += f"{i}\n"
        if color is None:
            color = "0x00ff00"
        embed = discord.Embed(title=title, description=newMessage, color=discord.Colour.from_str(color))
        await ctx.send("DONE")
        if footer is not None:
            embed.set_footer(text=footer)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        if image is not None:
            embed.set_image(url=image)
        if intro is not None:
            await channel.send(intro)
        await ctx.reply("Sending message to channel...", ephemeral = True)
        await channel.send(embed=embed)
    
    @embed.command(name='image', description = 'Send embeded image (using hex color)')
    async def embed_image(self, ctx, channel:discord.TextChannel, colour:str, image_url:str):
        embed = discord.Embed(color=discord.Colour.from_str(colour))
        embed.set_image(url=image_url)
        await ctx.reply("Sending message to channel...", ephemeral = True)
        await channel.send(embed=embed)
    
    @commands.hybrid_group(name='edit', description='Edit message/embed')
    async def edit_message(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.prefix}help edit")
    
    @edit_message.command(name='message', description="Edit bot's message")
    async def edit_msg(self, ctx:commands.Context, channel:discord.TextChannel, message_id, content:str):
        getMessage = await channel.fetch_message(message_id)
        await getMessage.edit(content=content)
        await ctx.send("Done", ephemeral=True)
    
    @edit_message.command(name='embed', description="Edit bot's embed message")
    async def edit_embed(self, ctx:commands.Context, channel:discord.TextChannel, message_id, title:str, message:str, color:str=None, footer:str=None, image:str=None,thumbnail:str=None):
        getEmbed = await channel.fetch_message(message_id)
        splitMessage = message.split('  ')
        newMessage = ''
        for i in splitMessage:
            newMessage += f"{i}\n"
        if color is None:
            color = "0x00ff00"
        embed = discord.Embed(title=title, description=newMessage, color=discord.Colour.from_str(color))
        await ctx.send("DONE")
        if footer is not None:
            embed.set_footer(text=footer)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        if image is not None:
            embed.set_image(url=image)
        await getEmbed.edit(embed=embed)
        await ctx.send("Done", ephemeral=True)

async def setup(client):
    await client.add_cog(broadcast(client))