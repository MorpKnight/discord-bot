import discord
from discord.ui import View
from discord.utils import get
from cogs.utility.ViewUtility import SingleRoleSelect, MultiRoleSelectEmoji

class GamesSelect(MultiRoleSelectEmoji):
    def __init__(self):
        self.role_list = ['Apex Legends', 'Genshin Impact', 'Valorant', 'Minecraft', 'Fate/Grand Order', 'osu!', 'Stumble', 'Mobile Legends', 'The Forest']
        self.emoji_list = ['<:apexlegends:1001616780860596305>', '<:genshinimpact:1001616581723422794>', '<:valorant:1001616587335422053>', '<:minecraft:1001616577680125982>',
        '<:fategrandorder:1001616585397649428>', '<:osu:1001616579852783716>', '<:stumble:1001616573271908412>', '<:mobilelegends:1001616571342540901>', '<:theforest:1066992765591887972>']
        super().__init__(
            placeholder= 'Your games!',
            role_list=self.role_list,
            emoji=self.emoji_list,
            max_values=len(self.role_list),
            custom_id='games'
        )

class KostSelect(SingleRoleSelect):
    def __init__(self):
        self.role_list = ['Kost', 'G Kost']
        super().__init__(
            placeholder="Kost?",
            role_list=self.role_list,
            custom_id="kost"
        )
class games(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GamesSelect())


class kost(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KostSelect())