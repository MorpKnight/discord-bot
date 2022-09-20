import time
import discord
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from cogs.utility.musicplayer import music_player, queue_button
from random import shuffle

class voicechannel(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
        self.queue = []
        self.voice_client = None
        self.voice_context = None
        self.now_playing = None
        self.looping = None
        self.time = 0
        self.playlist_spotify = []
        self.spotify_queue = []
        self.player = music_player()
        self.auto_disconnect.start()
    
    @commands.command(name='join', aliases=['j'], description='Join voice channel')
    async def join_voice(self, ctx:commands.Context):
        vc = ctx.author.voice
        if vc and vc.channel:
            if ctx.voice_client:
                await ctx.send(f"Already connected to {vc.channel}")
            else:
                try:
                    await vc.channel.connect()
                    self.voice_client = ctx.voice_client
                    self.voice_context = ctx
                    await ctx.send(f"Connected to {vc.channel}")
                except:
                    await ctx.send("Could not connect to voice channel")
        else:
            await ctx.send("You're not in voice channel")
    
    @commands.command(name='play', aliases=['p'], description='Play song on this bot')
    async def play_music(self, ctx:commands.Context, *, title:str=None):
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }
        vc = ctx.author.voice
        if vc and vc.channel:
            if ctx.voice_client:
                pass
            else:
                await vc.channel.connect()
                self.voice_client = ctx.voice_client
                self.voice_context = ctx
            
            if "spotify" in title:
                await self.player.get_spotify(title)
                if self.queue == []:
                    video = self.spotify_queue[0]
                    videoLookUp = self.player.search_song(title)
                    self.queue.append(videoLookUp)
                    self.spotify_queue.remove(video)
                    song_info = self.queue[0]
                    embed = discord.Embed(
                        title = "Playing...",
                        description = f"[{song_info['title']}]({song_info['webpage_url']})\n**Uploader:** {song_info['uploader']}",
                        color = discord.Color.random()
                    )
                    embed.set_thumbnail(url=song_info['thumbnail'])
                    self.voice_client.play(FFmpegPCMAudio(song_info['formats'][0]['url'], **FFMPEG_OPTIONS))
                    self.now_playing = song_info['title']
                    await ctx.send(embed=embed)
                    await self.player.get_time()
                    await self.player.next_queue()
                elif self.queue != []:
                    num = 0
                    description = ''
                    for i in self.queue:
                        num += 1
                        description += f"{num}. {i}\n"
                    embed = discord.Embed(
                        title='Adding song to queue',
                        description=description,
                        color=discord.Color.random()
                    )
                    await ctx.send(embed=embed)
                    await self.player.get_time()
            else:
                if self.queue != []:
                    video = self.player.search_song(title)
                    embed = discord.Embed(
                        title = 'Adding song to queue',
                        description = f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}",
                        color = discord.Color.random()
                    )
                    embed.set_thumbnail(url=video['thumbnail'])
                    await ctx.send(embed=embed)
                    self.queue.append(video)
                    await self.player.get_time()
                elif self.queue == []:
                    video = self.player.search_song(title)
                    embed = discord.Embed(
                        title = 'Playing...',
                        description = f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}",
                        color = discord.Color.random()
                    )
                    embed.set_thumbnail(url=video['thumbnail'])
                    self.voice_client.play(FFmpegPCMAudio(video['formats'][0]['url'], **FFMPEG_OPTIONS))
                    self.now_playing = video['title']
                    self.queue.append(video)
                    await ctx.send(embed=embed)
                    await self.player.get_time()
                    await self.player.next_queue()

    @commands.hybrid_command(name='leave', aliases=['dc', 'l'], description='Disconnect from voice channel')
    async def leave_channel(self, ctx:commands.Context):
        voiceChannel = ctx.voice_client
        if not voiceChannel:
            await ctx.send("Bot not in any voice channel")
        
        await voiceChannel.disconnect()
        await ctx.send(f"Disconnected from {voiceChannel.channel}")
    
    @commands.hybrid_command(name='stop', description = 'Stops the current song')
    async def stop_playing(self, ctx):
        voiceChannel = ctx.guild.voice_client
        if voiceChannel.is_playing():
            self.queue.clear()
            voiceChannel.stop()
            self.looping = False
            await ctx.send("Stopped from playing")
        else:
            await ctx.send("Nothing is playing")
    
    @commands.hybrid_command(name='skip', description = 'Skip to the next song')
    async def skip_song(self, ctx):
        # self.voice_client.stop()
        try:
            self.playlist_spotify.pop(0)
            await ctx.send("Skipped")
        except:
            await ctx.send("Nothing to skip")
    
    @commands.hybrid_command(name='loop', description = "Loop the current song")
    async def loop_song(self, ctx):
        if self.queue == []:
            fin = False
            if self.looping == False:
                if fin == False:
                    fin = True
                    self.looping = True
                    await ctx.send("Looping")
            elif self.looping == True:
                if fin == False:
                    fin = True
                    self.looping = False
                    await ctx.send("Stopped looping")
    
    @commands.hybrid_command(name='remove', description = 'Remove a song from the queue')
    async def remove_song(self, ctx, num:int):
        check = True
        items = 0
        for item in self.queue:
            if check != True:
                items += 1
            else:
                check = False
        if num <= items:
            if num <= 0:
                await ctx.send("Invalid number")
            else:
                video = self.queue[num]
                self.queue.remove(video)
                await ctx.send(f"Removed {video['title']}")
    
    @commands.hybrid_command(name='clear', description = 'Clears the queue')
    async def clear_queue(self, ctx):
        check = True
        for item in self.queue:
            if check == True:
                check = False
            else:
                self.queue.remove(item)
        for items in self.playlist_spotify:
            if check == True:
                check = False
            else:
                self.playlist_spotify.remove(items)
        await ctx.send("Cleared")
    
    @commands.hybrid_command(name='shuffle', description = 'Shuffles the queue')
    async def shuffle_queue(self, ctx):
        if self.queue != []:
            if self.spotify_queue != []:
                combine = list(self.queue[1:], self.spotify_queue[1:])
                shuffle(combine)
                self.queue[1:], self.spotify_queue[1:] = zip(*combine)
                await ctx.send("Shuffled")
            elif self.spot == []:
                shuffle(self.queue[1:])
                await ctx.send("Shuffled")
        else:
            await ctx.send("Nothing to shuffle")
    
    @commands.hybrid_command(name='queue', aliases=['q'], description = 'Shows the queue')
    async def show_queue(self, ctx):
        now = True
        n = 0
        desc = ""
        y = ""
        paginatedQueue = []
        formatedQueue = []
        currentPage = 0
        
        for item in self.queue:
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

        await ctx.send(embed=embed, view=queue_button(paginatedQueue))
    
    @tasks.loop(minutes=5)
    async def auto_disconnect(self):
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
                        self.queue = []
                        self.now_playing = None
                        self.looping = False
                        self.spotify_queue = []
                        self.playlist_spotify = []
            except AttributeError:
                pass

async def setup(client):
    await client.add_cog(voicechannel(client))