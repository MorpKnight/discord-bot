import asyncio

import discord
import requests
import spotipy
from discord import ButtonStyle, FFmpegPCMAudio
from discord.ext import commands
from discord.ui import View
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_dl import YoutubeDL

publicKey = 'ede84f6ac3964f8b84af9add65b5ea42'
secretKey = '31813713900f428dbe74ba438adaf19b'
clientManager = SpotifyClientCredentials(client_id=publicKey, client_secret=secretKey)
spotify = spotipy.Spotify(client_credentials_manager=clientManager)

class music_player():
    async def search_song(self, keyword):
        OPTION = {
            'format': 'bestaudio',
            'no_warnings': True,
            'default_search': 'auto',
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'geo_bypass': True,
            'quite': True,
            'noplaylist': True,
            'debug' : True
        }
        with YoutubeDL(OPTION) as ydl:
            try:
                requests.get(keyword)
            except:
                info = ydl.extract_info(f"ytsearch:{keyword}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(keyword, download=False)
        return info

    async def get_time(self):
        spotify_playlist = iter(self.spot)
        n = 1
        while self.voice_client.is_playing() == True:
            self.time += 1
            await asyncio.sleep(1)
            try:
                video = self.search_song(keyword=spotify_playlist.__next__())
                self.queue.append(video)
                n += 1
                if n == len(self.spotify_queue):
                    print("Done")
            except StopIteration:
                pass
        self.spot.clear()
    
    async def next_queue(self, ctx:commands.Context):
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        }
        while self.queue != []:
            if self.voice_client != None:
                if self.loop == False:
                    if self.voice_client.is_playing() == False:
                        if self.voice_client.is_paused() == False:
                            try:
                                self.queue.pop(0)
                            except:
                                pass
                            if self.queue != []:
                                self.time = 0
                                video = self.queue[0]
                                self.now_playing = video['title']
                                source = video['formats'][0]['url']
                                self.voice_client.play(FFmpegPCMAudio(source, **FFMPEG_OPTIONS))
                                embed = discord.Embed(
                                    title = "Now Playing",
                                    description = f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}",
                                    color = discord.Colour.random()
                                )
                                embed.set_thumbnail(url=video['thumbnail'])
                                await ctx.send(embed=embed)
                                await self.get_time()
                if self.loop == True:
                    if self.voice_client.is_playing() == False:
                        if self.voice_client.is_paused() == False:
                            self.time = 0
                            video = self.queue[0]
                            source = video['formats'][0]['url']
                            self.voice_client.play(FFmpegPCMAudio(source, **FFMPEG_OPTIONS))
                            embed = discord.Embed(
                                title = "Now Playing",
                                description=f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}",
                                color = discord.Colour.random()
                            )
                            await ctx.send(embed=embed)
                            await self.get_time()
            await asyncio.sleep(1)

    async def get_spotify(self, link):
        if "playlisy" in link:
            for track in spotify.playlist_tracks(link)["items"]:
                track_name = track["track"]["name"]
                track_artist = track["track"]["artists"][0]["name"]
                track_info = f"{track_name} by {track_artist}"
                self.spotify_queue.append(track_info)
        elif "album" in link:
            for track in spotify.album_tracks(link)["items"]:
                track_name = track["name"]
                track_artist = track["artists"][0]["name"]
                track_info = f"{track_name} by {track_artist}"
                self.spotify_queue.append(track_info)
        elif "artis" in link:
            result = spotify.artist_top_tracks(link)
            for track in result['tracks'][:10]:
                self.spotify_queue.append(track['name'])

class queue_button(View):
    def __init__(self, paginatedQueue):
        super().__init__(timeout = None)
        self.paginated = paginatedQueue
        self.currentPage = 0
        self.length = len(self.paginated) - 1
    
    async def updateButton(self, page:int):
        self.currentPage = page
        if page == 0:
            self.children[0].disabled = True
            self.children[1].disabled = False
        elif page == self.length:
            self.children[0].disabled = False
            self.children[1].disabled = True
        else:
            self.children[0].disabled = False
            self.children[1].disabled = False
        
    async def getPage(self, page:int, interaction:discord.Interaction):
        await self.updateButton(page)
        desc = ""
        for i in self.paginated[page]:
            desc = f"{i}\n"
        embed = discord.Embed(
            title = f'Queue for {interaction.guild.name}',
            description = desc,
            colour = discord.Colour.blue()
        )
        embed.set_footer(text=f"{page}/{self.length}")
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(
        label = 'back',
        style = discord.ButtonStyle.blurple,
        disabled = True
    )
    async def back(self, interaction:discord.Interaction, button):
        await self.getPage(self.currentPage - 1, interaction)
    
    @discord.ui.button(
        label = 'next',
        style = discord.ButtonStyle.blurple
    )
    async def next(self, interaction:discord.Interaction, button):
        await self.getPage(self.currentPage + 1, interaction)

    async def on_error(self, interaction:discord.Interaction, error, item):
        await interaction.response.edit_message(content=f"`{error}`")