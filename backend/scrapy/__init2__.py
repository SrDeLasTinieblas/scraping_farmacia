import random
import time
import requests
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures

# Crear una instancia de la clase BoticasPeru
boticas_salud = BoticasSalud("Boticas y Salud", "https://www.boticasysalud.com")

# Obtener la lista de categorías
#categoriesPeru = boticas_peru.get_categories()


categoriesSalud = boticas_salud.get_categories()
categoriesSalud = categoriesSalud[:1]
#print(categoriesSalud)
#print("\n")

for category_slug in categoriesSalud:
    products_slug = boticas_salud.get_product_urls(category_slug)
    for product_slug in products_slug[:10]:
        product = boticas_salud.get_product(product_slug)
        product.show_information()
        print("\n\n")
    

#print("Categories Salud")
#print(categoriesSalud)

#categories = categories[:2] #  --


final_products_url = []
categories_black_list = []
products_black_list = []










