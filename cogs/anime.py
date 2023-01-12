import discord
from discord import app_commands
from discord.app_commands import Choice, choices
from discord.ext import commands
from AnilistPython import Anilist
from mal import Anime, Manga, AnimeSearch, MangaSearch

class anime_manga(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def search_anime(self, interaction:discord.Interaction, title:str):
        animePage = AnimeSearch(title)
        result = Anime(animePage.results[0].mal_id)

        embed = discord.Embed(
            title = f"{result.title}; {result.title_japanese}; {result.title_english}",
            description = f"{result.synopsis}",
            color = discord.Color.random()
        )
        embed.add_field(name = "Type", value = f"{result.type} - {result.episodes} eps", inline = True)
        embed.add_field(name = "Studios", value = f"{result.studios}", inline = True)
        embed.add_field(name = "Premiered", value = f"{result.premiered}({result.aired})", inline = True)
        embed.add_field(name = "Score/Ranked", value = f"{result.score}/{result.rank}", inline = False)
        embed.add_field(name = "Source", value = f"{result.source}", inline = True)
        embed.add_field(name = "Status", value = f"{result.status}", inline = True)
        embed.add_field(name = "Genres", value = ", ".join(result.genres), inline = False)
        embed.set_thumbnail(url = result.image_url)
        embed.set_footer(text = f"[Click here]({result.url}) to access via MAL")

        return embed

    @app_commands.command(name='search', description="Search anime or manga in MyAnimeList")
    @app_commands.choices(format = [
        Choice(name="Anime", value="anime"),
        Choice(name="Manga", value="manga")
    ])
    async def search_anime_manga(self, interaction:discord.Interaction, format:Choice[str], title:str):
        if format.value == "anime":
            embed = await self.search_anime(interaction, title)
            await interaction.response.send_message(embed=embed)
            
        elif format.value == "manga":
            pass

async def setup(client):
    await client.add_cog(anime_manga(client))