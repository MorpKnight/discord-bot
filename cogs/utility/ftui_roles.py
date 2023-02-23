from discord.ui import View
from cogs.utility.ViewUtility import MultiRoleSelectEmoji, MultiRoleSelect, SingleRoleSelect

class GameSelect(MultiRoleSelectEmoji):
    def __init__(self):
        self.role_list = ['Valorant', 'Apex Legends', 'CS:GO', 'Genshin Impact', 'Rainbow Six Siege', 'Minecraft', 'PUBG PC', 'PUBGM', 'Fate/Grand Order', 'Dota 2', 'osu!']
        self.emoji_list = ['<:valorant:979988251215536179>', '<:apex:979987898071916565>', '<:csgo:979988255284002886>', '<:genshin:979988252905832468>', 
        '<:rainbowsix:979989238357557278>', '<:minecraft:979988672638226462>', '<:pubgpc:979988669970657330>', '<:pubgm:979988670721450014>', '<:fgo:980603043324256256>',
        '<:dota:986615940261232660>', '<:osu:986616086210437160>']
        super().__init__(
            placeholder="Choose your games",
            role_list=self.role_list,
            emoji=self.emoji_list,
            max_values=len(self.role_list),
            custom_id="games"
        )

class DepartemenSelect(SingleRoleSelect):
    def __init__(self):
        self.role_list = ['Dept. Teknik Sipil dan Lingkungan', 'Dept. Teknik Mesin', 'Dept. Teknik Elektro', 'Dept. Teknik Metalurgi dan Material', 'Dept. Teknik Arsitektur', 'Dept. Teknik Kimia', 'Dept. Teknik Industri', 'Program Internasional']
        super().__init__(
            placeholder="Choose your department",
            role_list=self.role_list,
            custom_id="departemen",
        )

class ProdiSelect(SingleRoleSelect):
    def __init__(self):
        self.role_list = ['Teknik Sipil', 'Teknik Lingkungan', 'Teknik Mesin', 'Teknik Perkapalan', 'Teknik Elektro', 'Teknik Komputer', 'Teknik Biomedik',
        'Teknik Metalurgi dan Material', 'Arsitektur', 'Arsitektur Interior', 'Teknik Kimia', 'Teknik Biopreoses', 'Teknik Industri']
        super().__init__(
            placeholder="Choose your program",
            role_list=self.role_list,
            custom_id="prodi",
        )

class AnimeSelecet(SingleRoleSelect):
    def __init__(self):
        self.role_list = ['Nimek Enjoyer']
        super().__init__(
            placeholder="Choose your anime",
            role_list=self.role_list,
            custom_id="anime",
        )

class games(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GameSelect())

class departemen(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DepartemenSelect())

class prodi(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ProdiSelect())

class animeenjoyer(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(AnimeSelecet())