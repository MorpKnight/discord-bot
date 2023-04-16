from tokenize import Single
from discord.ui import View
from cogs.utility.ViewUtility import SingleRoleSelect, MultiRoleSelect

class JobSelect(SingleRoleSelect):
    def __init__(self):
        self.role_list = ['PJ', 'WaPJ', 'Staff']
        super().__init__(
            placeholder="Posisi lo?",
            role_list=self.role_list,
            custom_id="job"
        )

class DivisiSelect(SingleRoleSelect):
    def __init__(self):
        self.role_list = ["Humas", "Publikasi", "Dokumentasi", "Desain", "Acara", "Dekorasi", "Konsumsi", "K3", "Transport Akomodasi", "Perlengkapan", "Danus"]
        super().__init__(
            placeholder="Divisi lo?",
            role_list=self.role_list,
            custom_id="divisi"
        )

class JobDivisiView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(JobSelect())
        self.add_item(DivisiSelect())