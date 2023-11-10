import random
import time

from pages.FarmaUniversal import FarmaUniversal

from pages.Inkafarma import Inkafarma

from pages.BoticasSalud import BoticasSalud

from pages.BoticasPeru import BoticasPeru

from pages.HogarSalud import HogarSalud


from pages.MiFarma import MiFarma
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

botica = BoticasPeru()
product_url = "https://boticasperu.pe/acondicionador-pantene-restauracion-frasco-400-ml.html"
products = botica.get_product(product_url)

for product in products:
    print(product.show_information())


#for category_url, category_title in categories.items():
#    print(category_title, ":", category_url)



"""

Testing Hogar y Salud



hogar_salud = HogarSalud()


categories = hogar_salud.get_categories()
print("categories", categories)


for categorie in categories[:1]:
    products_url = hogar_salud.get_product_urls(categorie)
    print("products_url", products_url)
    print("\n")
    for product_url in products_url[:20]:
        products = hogar_salud.get_product(product_url)
        for product in products:
            print(product.show_information())
            print("\n")

products = hogar_salud.get_product("https://www.hogarysalud.com.pe/producto/jeringa-desc-no-5-ml/")
for product in products:
    print(product.show_information2())


"""
