import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv, listdir
from cogs.utility.tekkomp_roles import game_roles, residence
from cogs.utility.serversma import rolebutton
from cogs.utility.ftui_roles import games, departemen, prodi, animeenjoyer
from cogs.utility.serverkuliah import games, kost, comic

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
        self.add_view(view=game_roles() ,message_id=1001619122838315139)
        self.add_view(view=residence(), message_id=1014667795239276605)
        self.add_view(view=rolebutton(), message_id=1001100602748715018)
        self.add_view(view=games(), message_id=1047116059632742433)
        self.add_view(view=kost(), message_id=1047116061759254630)
        self.add_view(view=comic(), message_id=1047116063554404352)


client = Client()
client.run(TOKEN)