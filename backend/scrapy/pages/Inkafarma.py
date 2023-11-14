from pages.base.BaseResponseFarma import BaseResponseFarma

class Inkafarma(BaseResponseFarma):
        
    code_farma = "MMPROD"
    code_company = "IKF"


    def __init__(self, id = 2, title = "Inkafarma", url = "https://inkafarma.pe/"):
        super().__init__(id, title, url)

    