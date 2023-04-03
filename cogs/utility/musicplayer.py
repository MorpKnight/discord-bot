import asyncio
from os import getenv

import discord
import requests
import spotipy
from discord import ButtonStyle, FFmpegPCMAudio
from discord.ui import Button, View, button
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import glob, os

load_dotenv()
publicKey = getenv("PUBLICKEY")
secretKey = getenv("SECRETKEY")
clientManager = SpotifyClientCredentials(client_id=publicKey, client_secret=secretKey)
spotify = spotipy.Spotify(client_credentials_manager=clientManager)

class musicPlayer():
    async def gettime(self):
        selfSpot = iter(self.spot)
        n = 1
        while self.voice_client.is_playing() == True:
            self.time += 1
            await asyncio.sleep(1)
            try:
                video = musicPlayer.search(query=selfSpot.__next__())
                self.query.append(video)
                n += 1
                if n == len(self.spot):
                    print("Done download all")
            except StopIteration:
                pass
        self.spot.clear()
    
    async def nextqueue(self, ctx):
        FFMPEG_OPTIONS = {
            'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
        }
        while self.query != []:
            if self.voice_client != None:
                if self.loop == False:
                    if self.voice_client.is_playing() == False:
                        if self.voice_client.is_paused() == False:
                            try:
                                self.query.pop(0)
                            except:
                                pass
                            if self.query != []:
                                self.time = 0
                                video = self.query[0]
                                self.np = video['title']
                                source = video['formats'][0]['url']
                                
                                # download song from url
                                YDL_OPT = {
                                    'format': 'bestaudio/best',
                                    "outtmpl": f"{video['title']}.mp3",
                                    "postprocessors": [
                                        {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
                                    ]
                                }

                                with yt_dlp.YoutubeDL(YDL_OPT) as ydl:
                                    ydl.download([video['webpage_url']])

                                songPath = max(glob.iglob(f"*.mp3"), key=os.path.getctime)
                                self.voice_client.play(FFmpegPCMAudio(songPath, **FFMPEG_OPTIONS)) 
                                # self.voice_client.play(FFmpegPCMAudio(source, **FFMPEG_OPTIONS))
                                embed = discord.Embed(
                                    title="Now playing", 
                                    description=f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}", 
                                    color=discord.Color.random())
                                embed.set_thumbnail(url=video['thumbnail'])
                                await ctx.send(embed=embed)
                                await musicPlayer.gettime(self)
                if self.loop == True:
                    if self.voice_client.is_playing() == False:
                        if self.voice_client.is_paused() == False:
                            self.time = 0
                            video = self.query[0]
                            source = video['formats'][0]['url']

                            # download song from url
                            YDL_OPT = {
                                'format': 'bestaudio/best',
                                "outtmpl": f"{video['title']}.mp3",
                                "postprocessors": [
                                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
                                ]
                            }

                            with yt_dlp.YoutubeDL(YDL_OPT) as ydl:
                                ydl.download([video['webpage_url']])

                            songPath = max(glob.iglob(f"*.mp3"), key=os.path.getctime)
                            self.voice_client.play(FFmpegPCMAudio(songPath, **FFMPEG_OPTIONS))
                            # self.voice_client.play(FFmpegPCMAudio(source, **FFMPEG_OPTIONS))
                            embed = discord.Embed(
                                title="Now playing",
                                description=f"[{video['title']}]({video['webpage_url']})\n**Uploader:** {video['uploader']}",
                                color=discord.Color.random())
                            await ctx.send(embed=embed)
                            await musicPlayer.gettime(self)
            await asyncio.sleep(1)
    
    def search(query):
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
        with yt_dlp.YoutubeDL(OPTION) as ydl:
            try:
                requests.get(query)
            except:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(query, download=False)
        return info
    
    async def spotify(self, link):
        if "playlist" in link:
            for track in spotify.playlist_tracks(link)["items"]:
                track_name = track["track"]["name"]
                track_artist = track["track"]["artists"][0]["name"]
                track_info = f"{track_name} by {track_artist}"
                self.spot.append(track_info)
        elif "album" in link:
            for track in spotify.album_tracks(link)["items"]:
                track_name = track["name"]
                track_artist = track["artists"][0]["name"]
                track_info = f"{track_name} by {track_artist}"
                self.spot.append(track_info)
        elif "artis" in link:
            result = spotify.artist_top_tracks(link)
            for track in result['tracks'][:10]:
                self.spot.appen(track['name'])
class queuebutton(View):
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