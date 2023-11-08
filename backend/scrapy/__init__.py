import random
import time
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.BoticasHogarSalud import BoticasHogarSalud
from pages.BoticasFarmaUniversal import BoticasFarmaUniversal
from pages.Mifarma import Mifarma
from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures



def download_product(page, product_url):
    tag = page.title 
    print(f"{tag} >>> Descargando product ", product_url)
    return product_url, page.get_product(product_url)


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
           
           for product_url in product_urls_internal:
               final_products_url.append(product_url) 
            
        else :
            categories_black_list.append(category_url)
       
        products_url_internal_size = len(product_urls_internal)
        print(f"{tag} >>> Cantidad de Products en Categoria :: {category_url} -> Tamaño :: {products_url_internal_size}")



    products_url_size = len(final_products_url)
    print(f"{tag} >>> Cantidad de Products Final :: {products_url_size}")

    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f"{tag} >>> Tiempo transcurrido de Obtener todos los urls products es : {tiempo_transcurrido:.2f} segundos")

    if len(categories_black_list) > 0:
        print(f"{tag} >>> Descargando nuevamente Categories de Black List")
        for category_black in categories_black_list:
            print(f"{tag} >>> Descargando Bkack Category : {category_black}")
            product_urls = page.get_product_urls(category_black)
            
            if not product_urls:
                print(f"{tag} >>> Productos nos descargados de black category {category_black}")
                continue
                        
            for product_url in product_urls:
                final_products_url.append(product_url)                  
            


    print(f"{tag} >>> Descargando Productos ....")

    unique_products_url = list(set(final_products_url))
    unique_products_url = unique_products_url[:5] # --FOR ACTION

    threaded_start = time.time()
    products = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for url in unique_products_url:
            futures.append(executor.submit(download_product, page=page, product_url=url))
        for future in concurrent.futures.as_completed(futures):
            product_url, product = future.result()
            if product:
                products.append(product)
            else:
                products_black_list.append(product_url)


    if len(products_black_list) > 0:
        print(f"{tag} >>> Descargando products de la Black List")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for url in products_black_list:
                futures.append(executor.submit(download_product, page=page, product_url=url))
            for future in concurrent.futures.as_completed(futures):
                product_url, product = future.result()
                if product:
                    products.append(product)
                else:
                    print(f"{tag} >>> Error al descargar -> black product {product_url}")


    print(f"{tag} >>> Descarga de productos finalizado : ", time.time() - threaded_start)

    for product in products:
        print("Nombre : ", product.name)
        print("Presentacion : ", product.presentation)
        print("Marca : ", product.brand)
        print("Precio por caja : ", product.price_box)
        print("Precio blister : ", product.price_blister)
        print("Fuente de Information : ", product.source_information)
        print("Lifting Date : ", product.lifting_date)
        print("Laboratory : ", product.laboratory)
        print("Card Discount : ", product.card_discount)
        print("Crossed Price : ", product.crossed_price)
        print("Suggested Comment : ", product.suggested_comment)
        print("-" * 20)
        print("\n")

## Call main

boticas_peru = BoticasPeru()
download_page_main(boticas_peru)

boticasSalud = BoticasSalud()
download_page_main(boticasSalud)

boticasHogarSalud = BoticasHogarSalud()
download_page_main(boticasHogarSalud)

#boticasFarmaUniversal = BoticasFarmaUniversal()
#download_page_main(boticasFarmaUniversal)



#mifarma = Mifarma()
#download_page_main(mifarma)

#print("Tamaño: ", len(mifarma.get_product_urls()))

#download_page_main(mifarma)



