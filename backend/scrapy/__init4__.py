import random
import time
import requests
from pages.BoticasFarmaUniversal import BoticasFarmaUniversal

from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures

# Crear una instancia de la clase BoticasPeru
botica_farma_universal = BoticasFarmaUniversal()

#categories = botica_farma_universal.get_categories()
#print(categories)

products_url = botica_farma_universal.get_product_urls("https://farmaciauniversal.com/productos/19-ofertas")
#print(products_url)

for producto_url in products_url:
    product = botica_farma_universal.get_product(producto_url)
    product.show_information()

#product = botica_farma_universal.get_product("https://farmaciauniversal.com/producto/detalle/209/354/nivea-men-invisible-blackwhite-power-antitranspirante-roll-on-x-50-ml")
#product.show_information()




