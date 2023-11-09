from pages.base.BaseResponseFarma import BaseResponseFarma

class BoticasInkafarma(BaseResponseFarma):
        
    code_farma = "MMPROD"
    code_company = "IKF"
    
    def __init__(self, title = "Inkafarma", url = "https://inkafarma.pe"):
        super().__init__(title, url)

    