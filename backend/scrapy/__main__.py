import random
import time

from pages.FarmaUniversal import FarmaUniversal
from pages.Inkafarma import Inkafarma
from pages.BoticasSalud import BoticasSalud
from pages.BoticasPeru import BoticasPeru
from pages.HogarSalud import HogarSalud
from pages.MiFarmaX import MiFarma
from pages.Digemid import Digemid

from model.Models import Product

from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures



"""
    Farmacia Universal  = 1
    Inkafarma           = 2
    Boticas y Salud     = 3
    Boticas Peru        = 4
    Hogar y Salud       = 5
    Digemin             = 6
    
"""

digemid = Digemid()


categories = digemid.get_categories()

for category in categories:
    product_ids = digemid.get_product_urls(category)
    for product_id in product_ids[:5]:
        products = digemid.get_product(product_id)
        for product in products:         
            product_more_detais = digemid.get_product_more_details(product)
            if not product_more_detais:
                continue
            
            product_more_detais.show_information2()
        


"""
                    For next call need data
                    codigoProducto":53725,"         ====> codProdE  ====> name
                    codEstablecimiento":"0053974"   ====> codEstab  ====> id_sku
                
                


               
                
# For More Datails :V

product = Product(
    id_sku = "0035291",
    name =  55019,
    presentation =  None,
    brand = None,
    price =  None,
    source_information = None,
    lifting_date =  None,
    laboratory =  None,
    card_discount = None,
    crossed_price =  None,
    suggested_comment =  None,
    description=None
)

product_more_detais = digemid.get_product_more_details(product)
product_more_detais.show_information2()

"""