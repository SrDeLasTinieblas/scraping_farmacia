import random
import time
import requests
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures

# Crear una instancia de la clase BoticasPeru
boticas_salud = BoticasSalud("Boticas y Salud", "https://www.boticasysalud.com")

categoriesSalud = boticas_salud.get_categories()
categoriesSalud = categoriesSalud[:1]

def concatenate_products(products):
    concatenated_data = "¬".join("|".join(str(getattr(product, attribute)) for attribute in 
                                          ["id_botica", "id_sku","name", "presentation", "brand", "price_box", "price_blister", 
                                           "source_information", "lifting_date", "laboratory", "card_discount", 
                                           "crossed_price", "suggested_comment"]) for product in products)
    return concatenated_data

products_slug = boticas_salud.get_product_urls("vitaminasysuplementos")  # Obtiene las URLs de productos

products = []  # Lista para almacenar objetos de productos

for product_slug in products_slug[:10]:
    product = boticas_salud.get_product(product_slug)  # Obtiene el objeto del producto
    products.append(product)  # Agrega el producto a la lista

# Concatena y muestra la información de los productos
concatenated_data = concatenate_products(products)
print(concatenated_data)










