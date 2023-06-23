import discord
from discord.ext import commands
from discord.utils import get


class memberjoin(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    
#     @commands.Cog.listener()
#     async def on_member_join(self, member:discord.Member):
#         if member.guild.id == 651392815204401152:
#             mainChannel = self.client.get_channel(651711390326849547)
#             mainRole = get(member.guild.roles, name='Member')
#             embed = discord.Embed(
#                 title='Welcome to the server!',
#                 description=f"""Hello {member.mention}!
#     Welcome to {member.guild.name}
#     Make sure you've read rules and guide in [here](https://discord.com/channels/651392815204401152/815406360799477811/1000008303729983518)
    
#     Thank you""",
#                 color=discord.Colour.random()
#             )
#             profile = discord.Embed(
#                 title="Some shit just landed here!",
#                 description=f"Welcome here ||{member.mention}||\nI don't hope you enjoy here",
#                 color=discord.Colour.random()
#             )
#             profile.set_thumbnail(url=member.avatar.url)
#             await member.add_roles(mainRole)
#             await member.send(embed=embed)
#             await mainChannel.send(embed=profile)

#         elif member.guild.id == 1001329512715391037:
#             mainChannel = self.client.get_channel(1001329539001110660)
#             mainRole = get(member.guild.roles, name='Mahasiswa')
#             embed = discord.Embed(
#                 title='Welcome to the server!',
#                 description=f"""Hello {member.mention}!
#     Welcome to {member.guild.name}
#     Make sure you've read rules and guide in [here](https://discord.com/channels/1001329512715391037/1001492836933447680/1001617805466157056)
    
#     Thank you""",
#                 color=discord.Colour.random()
#             )
#             profile = discord.Embed(
#                 title="Some shit just landed here!",
#                 description=f"Welcome here ||{member.mention}||\nI don't hope you enjoy here",
#                 color=discord.Colour.random()
#             )
#             profile.set_thumbnail(url=member.avatar.url)
#             await member.add_roles(mainRole)
#             await member.send(embed=embed)
#             await mainChannel.send(embed=profile)

#         elif member.guild.id == 979944957060214814:
#             welcomeChannel = get(member.guild.channels, id=979945731571990528)
#             newsChannel = get(member.guild.channels, id=980133552232480838)
#             rolesChannel = get(member.guild.channels, id=979947423982059600)
#             general = get(member.guild.channels, id=979947545721700372)
#             introChannel = get(member.guild.channels, id=980073335566241852)
#             message = f"""__**Ini adalah pesan otomatis**__
# Halo {member.mention}! Selamat datang di server **{member.guild.name}**.
# Perkenalkan saya adalah bot yang bertugas untuk membantu anda dalam mengatur server ini.
# Sebelumnya saya ucapkan selamat karena telah berhasil masuk Universitas Indonesia dengan prodi yang sudah dipilih
# Untuk info selanjutnya dapat dilihat pada {welcomeChannel.mention}
# Kemudian kamu dapat melihat berita terkini terkait update kuliah/kampus di {newsChannel.mention}
# Dan untuk mendapatkan role yang berkaitan dengan game yang kamu mainkan dapat dilihat pada {rolesChannel.mention}
# Jika ingin memperkenalkan diri kalian dapat lakukan di {introChannel.mention}

# Terima kasih atas kunjunganmu!"""

#             mahasiswaRole = get(member.guild.roles, name='Mahasiswa')
#             await member.add_roles(mahasiswaRole)

#             embed = discord.Embed(
#                 title='Selamat datang di server!',
#                 description=f'{message}',
#                 colour=discord.Colour.random()
#             )
#             embed.set_footer(text="Fakultas Teknik Universitas Indonesia")
#             for guild in self.client.guilds:
#                 if guild.id == 979944957060214814:
#                     try:
#                         await member.send(embed=embed)
#                     except:
#                         pass
            
#             profile = discord.Embed(
#                 title='Welcome!!',
#                 description=f"Selamat datang {member.mention} di server **{member.guild.name}**",
#                 colour=discord.Colour.random()
#             )
#             profile.set_thumbnail(url=member.avatar)
#             profile.set_footer(text="Fakultas Teknik Universitas Indonesia")
#             await general.send(embed=profile, delete_after=20)

#         elif member.guild.id == 964708141788962866:
#             pass
#         elif member.guild.id == 1042049711336591451:
#             mainchat = self.client.get_channel(1042049711852507218)
#             memberrole = get(member.guild.roles, name='Member')

#             embed = discord.Embed(
#                 title="地獄へようこそ!",
#                 description=f"Welcome here {member.mention}\nTunjukan jati dirimu sesungguhnya disini!\nHarap baca Rules & Guide di [sini](https://discord.com/channels/1042049711336591451/1042226755307569163/1042249203545542656)",
#                 color = discord.Colour.random()
#             )
#             embed.set_thumbnail(url=member.avatar.url)
#             await member.add_roles(memberrole)
#             await mainchat.send(embed=embed)


async def setup(client):
    await client.add_cog(memberjoin(client))