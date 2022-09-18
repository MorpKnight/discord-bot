import discord
from discord.ext import commands
from AnilistPython import Anilist

class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def animeFinder(self, title:str):
        finder = Anilist()
        anime = finder.get_anime(title)
        return anime
    
    async def animeInfo(self, title:str):
        anime = await self.animeFinder(title)
        
        genres = ", ".join(anime['genres'])
        titleRomaji = anime['name_romaji']
        titleEnglish = anime['name_english']
        image = anime['cover_image']
        format = anime['airing_format']
        status = anime['airing_status']
        eps = anime['airing_episodes']
        desc = anime['desc']
        desc = desc.replace("<br>", "")
        desc = desc.replace("<i>", "**")
        desc = desc.replace("</i>", "**")
        score:float = anime['average_score']/10
        season = anime['season']
        start = anime['starting_time']
        end = anime['ending_time']
        banner = anime['banner_image']
        return titleRomaji, titleEnglish, genres, image, format, status, eps, desc, score, season, start, end, banner
    
    async def embedAnime(self, ctx:commands.Context, title:str):
        titleRomaji, titleEnglish, genres, image, format, status, eps, desc, score, season, start, end, banner = await self.animeInfo(title)
        embed = discord.Embed(
            title = f"{titleRomaji}; {titleEnglish}",
            description=f"{desc}",
            color = discord.Colour.random()
        )
        embed.add_field(name='Start', value = f"{start}", inline=True)
        embed.add_field(name='End', value = f"{end}", inline=True)
        embed.add_field(name="Score", value=f"{score}", inline=True)
        embed.add_field(name="Season", value=f"{season}", inline=True)
        embed.add_field(name='Airing Format', value=f'{format}({eps} episodes)', inline=True)
        embed.add_field(name='Status', value=f"{status}", inline=True)
        embed.add_field(name="Genre", value=f"{genres}", inline=True)
        embed.set_image(url=f"{banner}")
        embed.set_thumbnail(url=f"{image}")
        await ctx.reply(embed=embed)
    
    async def mangaFinder(self, title:str):
        finder = Anilist()
        manga = finder.get_manga(title)
        return manga
    
    async def mangaInfo(self, title:str):
        manga = await self.mangaFinder(title)

        n = 0
        genres = ""
        for i in manga['genres']:
            if n == 0:
                genres += f"{i}"
            else:
                if n % 3 == 0:
                    genres += f"\n{i}"
                else:
                    genres += f", {i}"
            n += 1
    
        titleRomaji = manga['name_romaji']
        titleEnglish = manga['name_english']
        image = manga['cover_image']
        banner = manga['banner_image']
        format = manga['release_format']
        status = manga['release_status']
        chapter = manga['chapters']
        volume = manga['volumes']
        score:float = manga['average_score']/10
        desc = manga['desc']
        desc = desc.replace("<br>", "")
        desc = desc.replace("<i>", "**")
        desc = desc.replace("</i>", "**")
        return titleRomaji, titleEnglish, genres, image, format, status, chapter, volume, score, desc, banner
    
    async def embedManga(self, ctx:commands.Context, title:str):
        titleRomaji, titleEnglish, genres, image, format, status, chapter, volume, score, desc, banner = await self.mangaInfo(title)
        embed = discord.Embed(
            title = f"{titleRomaji}; {titleEnglish}",
            description=f"{desc}",
            color = discord.Colour.random()
        )
        embed.add_field(name="Genre", value=f"{genres}", inline=True)
        embed.add_field(name="Format", value=f"{format}", inline=True)
        embed.add_field(name="Status", value=f"{status}", inline=True)
        embed.add_field(name="Chapters", value=f"{chapter} Chapters", inline=True)
        embed.add_field(name="Volumes", value=f"{volume} Volumes", inline=True)
        embed.add_field(name="Score", value=f"{score}", inline=True)
        embed.set_image(url=f"{banner}")
        embed.set_thumbnail(url=f"{image}")
        await ctx.reply(embed=embed)
    
    @commands.hybrid_group(name='search', description = 'Search for anime or manga')
    async def search(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please specify an anime or manga')

    @search.command(name='anime', description = 'Search anime from Anilist')
    async def _searchanime(self, ctx, *, title:str):
        try:
            await self.embedAnime(ctx, title)
        except:
            await ctx.send("Anime not found")
    
    @search.command(name='manga', description = 'Search manga from Anilist')
    async def _searchmanga(self, ctx, *, title:str):
        try:
            await self.embedManga(ctx, title)
        except:
            await ctx.send("Manga not found or bad title")

async def setup(client):
    await client.add_cog(Anime(client))