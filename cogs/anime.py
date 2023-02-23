from asyncio import sleep
import asyncio

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from mal import Anime, AnimeSearch, Manga, MangaSearch


class anime_manga(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name='search', description='Search for an anime or manga')
    @app_commands.choices(media = [
        Choice(name='Anime', value='anime'),
        Choice(name='Manga', value='manga')
    ])
    async def search(self, interaction:discord.Interaction, media:Choice[str], title:str):
        await interaction.response.defer()
        while True:
            try:
                match media.value:
                    case 'anime':
                        search = AnimeSearch(title)
                        result_anime = Anime(search.results[0].mal_id)

                        title = f'{result_anime.title}; {result_anime.title_japanese}'
                        synopsis = f'{result_anime.synopsis}'
                        image_url = result_anime.image_url
                        type = result_anime.type
                        source = result_anime.source
                        score = result_anime.score
                        genres = ', '.join(result_anime.genres)
                        status = result_anime.status
                        episodes = result_anime.episodes
                        aired = result_anime.aired
                        duration = result_anime.duration
                        studios = ', '.join(result_anime.studios)
                        opening_themes = ', '.join(result_anime.opening_themes)
                        ending_themes = ', '.join(result_anime.ending_themes)
                        mal_id = result_anime.mal_id
                        url = result_anime.url

                        embed = discord.Embed(
                            title = title,
                            description = synopsis,
                            color = discord.Color.random()
                        )
                        embed.set_image(url=image_url)
                        embed.add_field(name='Type', value=type, inline=True)
                        embed.add_field(name='Source', value=source, inline=True)
                        embed.add_field(name='Score', value=score, inline=True)
                        embed.add_field(name='Status', value=f'{status}, {episodes} Ep.', inline=True)
                        embed.add_field(name='Aired', value=f'{aired}', inline=True)
                        embed.add_field(name='Genres', value=genres, inline=True)
                        embed.add_field(name='Studios', value=studios, inline=True)
                        embed.add_field(name='Opening Themes', value=opening_themes, inline=False)
                        embed.add_field(name='Ending Themes', value=ending_themes, inline=True)

                        embed.set_footer(text=f'ID: {mal_id}, URL: {url}')
                        await interaction.followup.send(embed=embed)

                    case 'manga':
                        search = MangaSearch(title)
                        result_manga = Manga(search.results[0].mal_id)

                        iamge_url = result_manga.image_url
                        title = f'{result_manga.title}; {result_manga.title_japanese}'
                        synopsis = f'{result_manga.synopsis}'
                        type = result_manga.type
                        score = result_manga.score
                        genres = ', '.join(result_manga.genres)
                        status = result_manga.status
                        volumes = result_manga.volumes
                        chapters = result_manga.chapters
                        published = result_manga.published
                        authors = ', '.join(result_manga.authors)
                        mal_id = result_manga.mal_id
                        url = result_manga.url

                        embed = discord.Embed(
                            title = title,
                            description = synopsis,
                            color = discord.Color.random()
                        )
                        embed.set_image(url=iamge_url)
                        embed.add_field(name='Type', value=type, inline=True)
                        embed.add_field(name='Score', value=score, inline=True)
                        embed.add_field(name='Genres', value=genres, inline=False)
                        embed.add_field(name='Status', value=f'{status}, {volumes} Volumes, {chapters} Chapters', inline=False)
                        embed.add_field(name='Published', value=f'{published}', inline=True)
                        embed.add_field(name='Authors', value=authors, inline=True)

                        embed.set_footer(text=f'ID: {mal_id}, URL: {url}')
                        await interaction.followup.send(embed=embed)
                break
            except:
                await asyncio.sleep(1)
                continue

async def setup(client):
    await client.add_cog(anime_manga(client))