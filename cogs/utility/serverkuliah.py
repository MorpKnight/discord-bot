from discord.ui import View
from cogs.utility.ViewUtility import MultiRoleSelect, SingleRoleSelect, RoleView

class GameSelect(MultiRoleSelect):
    def __init__(self):
        self.role_list = ['Apex Legends', 'VALORANT', 'Genshin Impact', 'Mobile Legends', 'osu!', 'GTA Online', 'The Forest', 'Clash Royale', 'TEKKEN', 'CS:GO']
        super().__init__(
            placeholder="Choose your games",
            role_list=self.role_list,
            max_values=len(self.role_list),
            custom_id="games"
        )

class KostSelect(SingleRoleSelect):
    def __init__(self):
        self.role_list = ['Kost', 'GaKost']
        super().__init__(
            placeholder="Kost?",
            role_list=self.role_list,
            custom_id="kost"
        )

class ComicSelect(MultiRoleSelect):
    def __init__(self):
        self.role_list = ['(H)Anime', 'Manga', 'Manhwa', 'Doujin']
        super().__init__(
            placeholder="Choose your comics",
            role_list=self.role_list,
            max_values=len(self.role_list),
            custom_id="comic"
        )
class KelasMPKT(SingleRoleSelect):
    def __init__(self):
        super().__init__(
            role_list=['MPKT 03', 'MPKT 04', 'MPKT 12', 'MPKT 21', 'MPKT 24', 'MPKT 29'],
            placeholder="Kelas MPKT",
            custom_id="kelas_mpkt"
        )
class KelasFismek(SingleRoleSelect):
    def __init__(self):
        super().__init__(
            role_list=['Fismek 03', 'Fismek 06', 'Fismek 08', 'Fismek 13', 'Fismek 15'],
            placeholder='Kelas Fisika Mekanika',
            custom_id='kelas_fismek'
        )

class KelasAlin(SingleRoleSelect):
    def __init__(self):
        super().__init__(
            role_list=['Aljabar Linear 05', 'Aljabar Linear 09', 'Aljabar Linear 13'],
            placeholder='Kelas Aljabar Linear',
            custom_id='kelas_alin'
        )

class KelasProgLan(SingleRoleSelect):
    def __init__(self):
        super().__init__(
            placeholder='Kelas Pemrograman Lanjut',
            role_list=['Proglan 01', 'Proglan 02'],
            custom_id='kelas_proglan'
        )

class KelasOAK(SingleRoleSelect):
    def __init__(self):
        super().__init__(
            placeholder='Kelas Organisasi dan Arsitektur Komputer',
            role_list=['OAK 01', 'OAK 02'],
            custom_id='kelas_oak'
        )

class Organisasi(SingleRoleSelect):
    def __init__(self):
        super().__init__(
            role_list=['IME', 'EXERCISE'],
            placeholder="Organisasi",
            custom_id="organisasi"
        )

class MatKulSodok(MultiRoleSelect):
    def __init__(self):
        super().__init__(
            role_list=['Kewirus', "Profet"],
            placeholder="Matkul Sodok",
            max_values=2,
            custom_id="matkul_sodok"
        )

class games(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GameSelect())

class kost(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KostSelect())

class comic(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ComicSelect())
class alin(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasAlin())
    
class fismek(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasFismek())

class mpkt(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasMPKT())

class proglan(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasProgLan())

class oak(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(KelasOAK())

class organisasi(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Organisasi())

class matkul_sodok(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MatKulSodok())