import random
import time
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.BoticasHogarSalud import BoticasHogarSalud
from pages.BoticasFarmaUniversal import BoticasFarmaUniversal
from pages.Mifarma import Mifarma
import concurrent.futures
import pyodbc
import os

# Obtener la cadena de conexión de la variable de entorno
conn_str = os.environ.get('SQL_SERVER_CONNECTION_STRING')

print(conn_str)

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
    unique_products_url = unique_products_url[:5]  # Limitar para pruebas

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
                product = future.result()
                if product:
                    products.append(product)
                else:
                    print(f"{tag} >>> Error al descargar -> black product {product_url}")

    print(f"{tag} >>> Descarga de productos finalizada en: ", time.time() - threaded_start)

    return products

def concatenate_products(products):
    concatenated_data = "¬".join("|".join(str(getattr(product, attribute)) for attribute in ["name", "presentation", "brand", "price_box", "price_blister", "source_information", "lifting_date", "laboratory", "card_discount", "crossed_price", "suggested_comment"]) for product in products)
    return concatenated_data

if __name__ == '__main__':
    boticas_peru = BoticasPeru()
    boticas_salud = BoticasSalud()
    boticas_hogar_salud = BoticasHogarSalud()

    products_peru = download_page_main(boticas_peru)
    products_salud = download_page_main(boticas_salud)
    products_hogar_salud = download_page_main(boticas_hogar_salud)

    concatenated_data = concatenate_products(products_peru + products_salud + products_hogar_salud)

    # Imprimir o guardar la variable concatenated_data según tus necesidades
    #print(concatenated_data)
    
    # Establece la conexión
    conn = pyodbc.connect(conn_str)

    # Crea un cursor
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO productos (productos)
    VALUES (?)
    """
    cursor.execute(insert_query, concatenated_data)
    conn.commit()
        
    # Cierra el cursor y la conexión
    cursor.close()
    conn.close()





