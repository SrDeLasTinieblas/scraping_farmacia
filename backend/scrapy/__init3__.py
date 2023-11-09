import random
import time
import requests
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.BoticasHogarSalud import BoticasHogarSalud

from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures

# Crear una instancia de la clase BoticasPeru
boticas_peru = BoticasPeru()
boticas_salud = BoticasSalud()
boticas_hogar_salud = BoticasHogarSalud()

# Obtener la lista de categorías
"""
categories_hogar_salud = boticas_hogar_salud.get_categories()

print(categories_hogar_salud)

categories_hogar_salud = categories_hogar_salud[:1]

for category_url in categories_hogar_salud:
    products_url = boticas_hogar_salud.get_product_urls(category_url)
    print(products_url)


#categories = categories[:2] #  --


final_products_url = []
categories_black_list = []
products_black_list = []


"""

categories_hogar_salud = boticas_hogar_salud.get_categories()

categories_hogar_salud = categories_hogar_salud[:1]

for category_url in categories_hogar_salud:
    products_url = boticas_hogar_salud.get_product_urls(category_url)
    for product_url in products_url:
        product = boticas_hogar_salud.get_product(product_url)
        product.show_information()
    #print(products_url)


#categories = categories[:2] #  --

#product_url = "https://www.hogarysalud.com.pe/producto/panal-para-adulto-tena-slip-ultra-talla-l-paquete-21-un/"
#product = boticas_hogar_salud.get_product(product_url)
#product.show_information()






