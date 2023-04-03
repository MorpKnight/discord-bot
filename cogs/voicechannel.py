import time
from random import shuffle
import glob, os

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
from discord.ui import View
import yt_dlp

from cogs.utility.musicplayer import musicPlayer, queuebutton


class voice(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.query = []
        self.voice_client = None
        self.voice_context = None
        self.np = None
        self.loop = False
        self.time = 0
        self.playlist = []
        self.spot = []
        self.autodisconnect.start()
    
    @commands.hybrid_command(name='join', aliases=['j'], description = 'Join the voice channel')
    async def _join(self, ctx):
        voiceChannel = ctx.author.voice
        if voiceChannel and voiceChannel.channel:
            if ctx.voice_client:
                await ctx.send(f"Already connected to {voiceChannel.channel}")
            else:
                try:
                    await voiceChannel.channel.connect()
                    self.voice_client = ctx.voice_client
                    self.voice_context = ctx
                    await ctx.send(f"Connected to {voiceChannel.channel}")
                except:
                    await ctx.send("Could not connect to voice channel")
        else:
            await ctx.send("You are not in a voice channel")
    
    @commands.hybrid_command(name='play', aliases=['p'], description = "Plays a song")
    async def _play(self, ctx, *, title:str=None):
        FFMPEG_OPTIONS = {
        'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
        }
        voiceChannel = ctx.author.voice
        if voiceChannel and voiceChannel.channel:
            if ctx.voice_client:
                pass
            else:
                await voiceChannel.channel.connect()
                self.voice_client = ctx.voice_client
                self.voice_context = ctx
            if "spotify" in title:
                await musicPlayer.spotify(self, link=title)
                if self.query == []:
                    video = self.spot[0]
                    videoLookUp = musicPlayer.search(query=video)
                    self.query.append(videoLookUp)
                    self.spot.remove(video)
                    query = self.query[0]
                    embed = discord.Embed(
                        title = "Playing...",
                        description = f"[{query['title']}]({query['webpage_url']})\n**Uploader:** {query['uploader']}",
                        color = discord.Color.random()
                    )
                    embed.set_thumbnail(url=query['thumbnail'])
                    self.voice_client.play(FFmpegPCMAudio(query['formats'][0]['url'], **FFMPEG_OPTIONS))
                    self.np = query['title']
                    await ctx.send(embed=embed)
                    await musicPlayer.gettime(self)
                    await musicPlayer.nextqueue(self, ctx)
                elif self.query != []:
                    num = 0
                    description = ''
                    for i in self.query:
                        num += 1
                        description += f"{num}. {i}\n"
                    embed = discord.Embed(
                        title='Adding song to queue',
                        description=description,
                        color=discord.Color.random()
                    )
                    await ctx.send(embed=embed)
                    await musicPlayer.gettime(self)
            else:
                if self.query != []:
                    video = musicPlayer.search(query=title)
                    embed = discord.Embed(
                        title = 'Adding song to queue',
                        description = f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}",
                        color = discord.Color.random()
                    )
                    embed.set_thumbnail(url=video['thumbnail'])
                    await ctx.send(embed=embed)
                    self.query.append(video)
                    await musicPlayer.gettime(self)
                elif self.query == []:
                    video = musicPlayer.search(title)
                    embed = discord.Embed(
                        title = 'Playing...',
                        description = f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}",
                        color = discord.Color.random()
                    )
                    embed.set_thumbnail(url=video['thumbnail'])
                    self.voice_client.play(FFmpegPCMAudio(video['url'], **FFMPEG_OPTIONS))
                    self.np = video['title']
                    self.query.append(video)
                    await ctx.send(embed=embed)
                    await musicPlayer.gettime(self)
                    await musicPlayer.nextqueue(self, ctx)
    
    @commands.hybrid_command(name='leave', aliases=['dc', 'l'], description = 'Disconnects from the voice channel')
    async def _leave(self, ctx:commands.Context):
        voiceChannel = ctx.voice_client
        if not voiceChannel:
            await ctx.send("Bot not in any voice channel")
        
        await voiceChannel.disconnect()
        await ctx.send(f"Disconnected from {voiceChannel.channel}")
        # if channel and channel.channel:
        #     if ctx.voice_client:
        #         if channel.channel == ctx.voice_client.channel:
        #             try:
        #                 if ctx.voice_client.is_palying():
        #                     ctx.voice_client.stop()
        #                     await ctx.voice_client.disconnect()
        #                     await ctx.send("Disconnected from voice channel")
        #                     try:
        #                         self.voice_client = None
        #                         self.voice_context = None
        #                         self.query = []
        #                         self.np = None
        #                         self.loop = False
        #                         self.time = 0
        #                         self.playlist = []
        #                         self.spot = []
        #                     except:
        #                         pass
        #                 else:
        #                     await ctx.voice_client.disconnect()
        #                     await ctx.send(f"Disconnected from voice {channel.channel}")
        #             except:
        #                 await ctx.send("Could not disconnect from voice channel")
        #         else:
        #             await ctx.send("You're not in the same voice channel")
        #     else:
        #         await ctx.send("You're not in a voice channel")
    
    @commands.hybrid_command(name='stop', description = 'Stops the current song')
    async def _stop(self, ctx):
        voiceChannel = ctx.guild.voice_client
        if voiceChannel.is_playing():
            self.query.clear()
            voiceChannel.stop()
            self.loop = False
            await ctx.send("Stopped from playing")
        else:
            await ctx.send("Nothing is playing")
    
    @commands.hybrid_command(name='skip', description = 'Skip to the next song')
    async def _skip(self, ctx):
        self.voice_client.stop()
        try:
            self.playlist.pop(0)
            await ctx.send("Skipped")
        except:
            await ctx.send("Nothing to skip")
    
    @commands.hybrid_command(name='loop', description = "Loop the current song")
    async def _loop(self, ctx):
        if self.query == []:
            fin = False
            if self.loop == False:
                if fin == False:
                    fin = True
                    self.loop = True
                    await ctx.send("Looping")
            elif self.loop == True:
                if fin == False:
                    fin = True
                    self.loop = False
                    await ctx.send("Stopped looping")
    
    @commands.hybrid_command(name='remove', description = 'Remove a song from the queue')
    async def _remove(self, ctx, num:int):
        check = True
        items = 0
        for item in self.query:
            if check != True:
                items += 1
            else:
                check = False
        if num <= items:
            if num <= 0:
                await ctx.send("Invalid number")
            else:
                video = self.query[num]
                self.query.remove(video)
                await ctx.send(f"Removed {video['title']}")
    
    @commands.hybrid_command(name='clear', description = 'Clears the queue')
    async def _clear(self, ctx):
        check = True
        for item in self.query:
            if check == True:
                check = False
            else:
                self.query.remove(item)
        for items in self.playlist:
            if check == True:
                check = False
            else:
                self.playlist.remove(items)
        await ctx.send("Cleared")
    
    @commands.hybrid_command(name='shuffle', description = 'Shuffles the queue')
    async def _shuffle(self, ctx):
        if self.query != []:
            if self.spot != []:
                combine = list(self.query[1:], self.spot[1:])
                shuffle(combine)
                self.query[1:], self.spot[1:] = zip(*combine)
                await ctx.send("Shuffled")
            elif self.spot == []:
                shuffle(self.query[1:])
                await ctx.send("Shuffled")
        else:
            await ctx.send("Nothing to shuffle")
        
    @commands.hybrid_command(name='queue', aliases=['q'], description = 'Shows the queue')
    async def _queue(self, ctx):
        now = True
        n = 0
        desc = ""
        y = ""
        paginatedQueue = []
        formatedQueue = []
        currentPage = 0
        
        for item in self.query:
            if now != True:
                n += 1
                y = time.strftime('%H:%M:%S', time.gmtime(int(item["duration"])))
                songFormated = f"`{n}.` `{item['title']} `\n`{y}` `Uploaded by : {item['uploader']}`\n"
                formatedQueue.append(songFormated)
            else:
                now = False
                y = time.strftime('%H:%M:%S', time.gmtime(int(item["duration"])))
                songFormated =  f'`Now Playing: `\n`{item["title"]} `\n`{y}` `Uploaded by : {item["uploader"]}`\n\n'
                formatedQueue.append(songFormated)
        
        for i in range(0, len(formatedQueue), 20):
            paginatedQueue.append(formatedQueue[i:i+20])
        total_page = len(paginatedQueue)
        for j in paginatedQueue[currentPage]:
            desc += j + "\n"
        
        embed = discord.Embed(title='Queue', description=desc, color=discord.Colour.blue())
        embed.set_footer(text=f'Page {currentPage+1}/{total_page}')

        await ctx.send(embed=embed, view=queuebutton(paginatedQueue))
    
    @commands.hybrid_command(name="nowplaying", aliases=['np'], description="Shows what song is playing")
    async def now_playing(self, ctx:commands.Context):
        embed = discord.Embed(
            title="Now Playing",
            description=self.np,
            color=discord.Colour.random()
        )
        await ctx.reply(embed=embed)
    
    @tasks.loop(minutes=5)
    async def autodisconnect(self):
        for guild in self.client.guilds:
            channelConnected:discord.VoiceClient = guild.voice_client
            try:
                if channelConnected.is_connected():
                    if channelConnected.is_playing():
                        pass
                    elif channelConnected.is_paused():
                        pass
                    else:
                        await channelConnected.disconnect()
                        await self.voice_context.send("Disconnected from voice channel")
                        self.voice_client = None
                        self.voice_context = None
                        self.query = []
                        self.np = None
                        self.loop = False
                        self.spot = []
                        self.playlist = []
            except AttributeError:
                pass


async def setup(client):
    await client.add_cog(voice(client))