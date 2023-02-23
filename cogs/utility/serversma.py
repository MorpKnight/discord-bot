from discord.ui import View
from cogs.utility.ViewUtility import MultiRoleSelectEmoji

class GameSelect(MultiRoleSelectEmoji):
    def __init__(self):
        self.role_list = ['Genshin Impact', 'Rainbow Six Siege', 'Apex Legends', 'Fate/Grand Order', 'Valorant', 'Dota 2', 'osu!', 'Mobile Legend']
        self.emoji_list = ['<:genshin:815419235748544564>', '<:rainbow6:815421287206879253>', '<:apexlegends:815419103278792714>', '<:fgo:957039392910884924>',
        '<:valorant:815419012636475403>', '<:dota:957043427172819014>', '<:osu:815540842986864640>', '<:ml:957043516343746580>']
        super().__init__(
            placeholder="Choose your games",
            role_list=self.role_list,
            emoji=self.emoji_list,
            max_values=len(self.role_list),
            custom_id="games"
        )

class games(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GameSelect())