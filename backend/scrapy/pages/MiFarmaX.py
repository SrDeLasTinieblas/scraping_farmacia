from pages.base.BaseResponseFarma import BaseResponseFarma

class MiFarma(BaseResponseFarma):    
    code_farma = "MMMFPRD"
    code_company = "MF" 
          
    def __init__(self, title = "Mi farma", url = "https://www.mifarma.com.pe"):
        super().__init__(id, title, url)

