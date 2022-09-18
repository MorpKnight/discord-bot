import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv, listdir

load_dotenv()
TOKEN = getenv('TOKEN')

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or('.'),
            case_insensitive = True,
            intents = discord.Intents.all()
        )
    
    async def startup(self):
        await client.wait_until_ready()
        await client.tree.sync()
    
    async def setup_hook(self):
        for filename in listdir("./cogs"):
            if filename.endswith(".py"):
                name = filename[:-3]
                await client.load_extension(f"cogs.{name}")
        self.loop.create_task(self.startup())

client = Client()
client.run(TOKEN)