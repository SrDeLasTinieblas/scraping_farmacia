import random
import time
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.HogarSalud import HogarSalud
from pages.FarmaUniversal import FarmaUniversal
from pages.MiFarmaX import MiFarma
from pages.Inkafarma import Inkafarma
from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures

def download_product(page, product_url):
    tag = page.title 
    print(f"{tag} >>> Descargando producto ", product_url)
    return page.get_product(product_url)

def download_page_main(page):     
    tag = page.title 
    inicio = time.time()

    final_products_url = []
    products_black_list = []
    categories_black_list = []

    categories = page.get_categories()
    categories = categories[:1]  # Limitar a una categoría (para pruebas)

    for category_url in categories:               
        product_urls_internal = page.get_product_urls(category_url)  
        if product_urls_internal:
            final_products_url.extend(product_urls_internal) 
        else:
            categories_black_list.append(category_url)

        products_url_internal_size = len(product_urls_internal)
        print(f"{tag} >>> Cantidad de Productos en Categoría :: {category_url} -> Tamaño :: {products_url_internal_size}")

    products_url_size = len(final_products_url)
    print(f"{tag} >>> Cantidad de Productos Final :: {products_url_size}")

    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"{tag} >>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")

    if len(categories_black_list) > 0:
        print(f"{tag} >>> Descargando nuevamente categorías de Black List")
        for category_black in categories_black_list:
            print(f"{tag} >>> Descargando Black Category : {category_black}")
            product_urls = page.get_product_urls(category_black)

            if not product_urls:
                print(f"{tag} >>> Productos no descargados de la black category {category_black}")
                continue

            final_products_url.extend(product_urls)

    print(f"{tag} >>> Descargando Productos ....")

    unique_products_url = list(set(final_products_url))
    unique_products_url = unique_products_url[:10]  # Limitar para pruebas

    threaded_start = time.time()
    products = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_product, page, product_url): product_url for product_url in unique_products_url}
        for future in concurrent.futures.as_completed(futures):
            product_url = futures[future]
            product = future.result()
            if product:
                products.append(product)
            else:
                products_black_list.append(product_url)

    if len(products_black_list) > 0:
        print(f"{tag} >>> Descargando productos de la Black List")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(download_product, page, product_url): product_url for product_url in products_black_list}
            for future in concurrent.futures.as_completed(futures):
                product_url = futures[future]
                products_internal = future.result()
                if products_internal:
                    # Recuerda que ahora ya no traer un solo producto
                    # sino un array de products, por eso recorremos
                    for product_internal in products_internal:
                        products.append(product_internal)
                else:
                    print(f"{tag} >>> Error al descargar -> black product {product_url}")

    print(f"{tag} >>> Descarga de productos finalizada en: ", time.time() - threaded_start)

    return products

def concatenate_products(products):
    concatenated_data = "¬".join(product.show_information() for product in products)
    return concatenated_data



'''
        print("SKU#: ", )
        print("Nombre : ", product.name)
        print("Presentacion : ", product.presentation)
        print("Marca : ", product.brand)
        print("Precio por caja : ", product.price)
        print("Fuente de Information : ", product.source_information)
        print("Lifting Date : ", product.lifting_date)
        print("Laboratory : ", product.laboratory)
        print("Card Discount : ", product.card_discount)
        print("Crossed Price : ", product.crossed_price)
        print("Suggested Comment : ", product.suggested_comment)
        print("-" * 20)
        
        print("\n")
        '''

## Call main
'''
boticas_mifarma = BoticasMiFarma()
products_mifarma = download_page_main(boticas_mifarma)

boticas_inkafarma = BoticasInkafarma()
products_inkafarma = download_page_main(boticas_inkafarma)

BoticasHogarSalud = BoticasHogarSalud()
productosHogarSalud = download_page_main(BoticasHogarSalud)

BoticasFarmaUniversal = BoticasFarmaUniversal()
productosHogarSalud = download_page_main(BoticasFarmaUniversal)

boticas_peru = BoticasPeru()
products_peru = download_page_main(boticas_peru)

boticas_salud = BoticasSalud()
products_salud = download_page_main(boticas_salud)
'''

boticas_peru = BoticasPeru()
products_peru = download_page_main(boticas_peru)

#boticasHogarSalud = BoticasHogarSalud()
#productosHogarSalud = download_page_main(boticasHogarSalud)

#print(boticasHogarSalud.get_all_products_in_category("https://www.boticasysalud.com/tienda/catalogo/vitaminasysuplementos"))

'''
boticas_salud = BoticasSalud()
products_salud = download_page_main(boticas_salud)

BoticasHogarSalud = BoticasHogarSalud()
productosHogarSalud = download_page_main(BoticasHogarSalud)

boticas_mifarma = BoticasMiFarma()
products_mifarma = download_page_main(boticas_mifarma)

boticas_inkafarma = BoticasInkafarma()
products_inkafarma = download_page_main(boticas_inkafarma)
'''


concatenated_data = concatenate_products(products_peru)
#

print(concatenated_data)







