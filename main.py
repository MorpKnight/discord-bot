import importlib
from os import getenv, listdir

import discord
import yaml
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')

with open("config.yml", "r") as f:
    data = yaml.safe_load(f)
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
        for i in data['Roles']:
            # global module
            for key, value in data['Roles'][i].items():
                if key == 'filename':
                    module = importlib.import_module(f"cogs.utility.{value}")
                else:
                    class_ = getattr(module, key)
                    self.add_view(view=class_(), message_id=value)


client = Client()
client.run(TOKEN)