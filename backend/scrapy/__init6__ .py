import random
import time
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.BoticasHogarSalud import BoticasHogarSalud
from pages.BoticasFarmaUniversal import BoticasFarmaUniversal
from pages.BoticasInkafarma import BoticasInkafarma
from utils.NetUtils import download_page, get_random_user_agent


botica_inkafarma = BoticasInkafarma()
categories_id = botica_inkafarma.get_categories()
print("categories", categories_id)
print()


for category_id in categories_id[:1]:
    products_id = botica_inkafarma.get_product_urls(category_id)
    print("products_id", products_id)
    random_product_id = random.choice(products_id)
    product = botica_inkafarma.get_product(random_product_id)
    product.show_information()

