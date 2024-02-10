import asyncio

import discord
from discord.ext import commands


class message_nocommand(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.client.user:
            pass

        elif message.channel.id == 964734550536228904:
            FTUI_channel = self.client.get_channel(980133552232480838)
            await message.publish()
            try:
                await FTUI_channel.send(content=message.content, embeds=message.embeds)
                if message.channel.id == 980133552232480838:
                    await message.publish()
                else:
                    pass
            except:
                pass
        
        elif message.channel.id == 992383737998352465:
            if "gio" in message.content:
                await message.delete()
            else:
                anonymousChannel = self.client.get_channel(1011113637496242279)
                formated_message = f"`{message.content}`"
                embed_message = discord.Embed(description=formated_message)
                await anonymousChannel.typing()
                await anonymousChannel.send(embed=embed_message)
                await asyncio.sleep(0.5)
                await message.delete()

                anonymouslog = self.client.get_channel(1011982504904900609)
                await anonymouslog.send(f"`{message.content}` ~ {message.author.global_name}")
        
        elif message.channel.id == 1011113637496242279:
            if message.author.id == 385053392059236353:
                pass
            else:
                if message.type == discord.MessageType.reply:
                    if message.author == self.client.user:
                        pass
                    else:
                        if "gio" in message.content:
                            await message.delete()
                        else:
                            fetchMessage = message.channel.get_partial_message(message.reference.resolved.id)
                            await asyncio.sleep(0.2)
                            await message.delete()
                            embed_message = discord.Embed(description=f"`{message.content}`")
                            await fetchMessage.reply(embed=embed_message)

                            anonymouslog = self.client.get_channel(1011982504904900609)
                            await anonymouslog.send(f"`{message.content}` ~ {message.author.global_name}")
                else:
                    if "gio" in message.content:
                            await message.delete()
                    else:
                        await asyncio.sleep(0.2)
                        await message.delete()
                        embed_message = discord.Embed(description=f"`{message.content}`")
                        await message.channel.send(embed=embed_message)

                        anonymouslog = self.client.get_channel(1011982504904900609)
                        await anonymouslog.send(f"`{message.content}` ~ {message.author.global_name}")
                
        elif message.channel.id == 964734223590260736:
            await message.add_reaction("👋")

        elif message.channel.type == discord.ChannelType.private:
            anonymousChannel = self.client.get_channel(1011113637496242279)
            if message.content.startswith("$anonym"):
                pass
            else:
                await message.channel.send(f"Untuk dapat mengirimkan pesan ke {anonymousChannel.mention} harap gunakan `$anonym` atau `/anonym`")
        
        elif message.guild.id == 964708141788962866:
            if message.channel.id == 964719963204104242:
                pass
            else:
                if "gio" in message.content:
                    await message.delete()

async def setup(client):
    await client.add_cog(message_nocommand(client))