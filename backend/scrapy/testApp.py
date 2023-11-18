import inquirer
from model.Models import Product
from pages.FarmaUniversal import FarmaUniversal
from pages.Inkafarma import Inkafarma
from pages.MiFarmaX import MiFarma
from pages.BoticasSalud import BoticasSalud
from pages.BoticasPeru import BoticasPeru
from pages.HogarSalud import HogarSalud
from utils.UploadDatabase import upload_to_db
import concurrent.futures
import numpy as np
import time

def download_product(botica, product_url):
    tag = botica.title 
    print(f"{tag} >>> Descargando producto ", product_url)
    return product_url, botica.get_product(product_url)

def scrape_selected_pages(selected_pags):
    boticas = []
    
    #print(boticas)
    
    # Crear instancias fuera del bucle
    botica_salud = BoticasSalud()
    botica_peru = BoticasPeru()
    hogar_salud = HogarSalud()
    farmacia_universal = FarmaUniversal()
    inkafarma = Inkafarma()
    mi_farma = MiFarma()

    for pag in selected_pags:
        if pag['value'] == botica_salud.url:
            categories = botica_salud.get_categories()
            total_categories = len(categories)
            print(f"Tamaño de categorías en {pag['name']}: {total_categories}")

            total_products = 0
            for category_url in categories:
                total_products += len(botica_salud.get_product_urls(category_url))
            print(f"Tamaño total de productos en {pag['name']}: {total_products}")

        elif pag['value'] == botica_peru.url:
            categories = botica_peru.get_categories()
            total_categories = len(categories)
            print(f"Tamaño de categorías en {pag['name']}: {total_categories}")

            total_products = 0
            inicio = time.time()

            for category_url in categories:
                total_products += len(botica_peru.get_product_urls(category_url))
            print(f"Tamaño total de productos en {pag['name']}: {total_products}")
            fin = time.time()
            tiempo_transcurrido = fin - inicio
            print(f">>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")
        
        elif pag['value'] == hogar_salud.url:
            categories = hogar_salud.get_categories()
            #print("categorias", categories)
            total_categories = len(categories)
            print(f"Tamaño de categorías en {pag['name']}: {total_categories}")

            total_products = 0
            inicio = time.time()

            for category_url in categories:
                total_products += len(hogar_salud.get_product_urls(category_url))
            print(f"Tamaño total de productos en {pag['name']}: {total_products}")
            fin = time.time()
            tiempo_transcurrido = fin - inicio
            print(f">>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")
        
        
        elif pag['value'] == farmacia_universal.url:
            categories = farmacia_universal.get_categories()
            total_categories = len(categories)
            print(f"Tamaño de categorías en {pag['name']}: {total_categories}")

            total_products = 0
            inicio = time.time()

            for category_url in categories:
                print("category url: ", category_url)
                total_products += len(farmacia_universal.get_product_urls(category_url))
            print(f"Tamaño total de productos en {pag['name']}: {total_products}")
            fin = time.time()
            tiempo_transcurrido = fin - inicio
            print(f">>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")
        
        elif pag['value'] == inkafarma.url:
            categories = inkafarma.get_categories()
            total_categories = len(categories)
            print(f"Tamaño de categorías en {pag['name']}: {total_categories}")

            total_products = 0
            inicio = time.time()

            for category_url in categories:
                total_products += len(inkafarma.get_product_urls(category_url))
            print(f"Tamaño total de productos en {pag['name']}: {total_products}")
            fin = time.time()
            tiempo_transcurrido = fin - inicio
            print(f">>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")
        
        elif pag['value'] == mi_farma.url:
            categories = mi_farma.get_categories()
            total_categories = len(categories)
            print(f"Tamaño de categorías en {pag['name']}: {total_categories}")

            total_products = 0
            inicio = time.time()

            for category_url in categories:
                total_products += len(mi_farma.get_product_urls(category_url))
            print(f"Tamaño total de productos en {pag['name']}: {total_products}")
            fin = time.time()
            tiempo_transcurrido = fin - inicio
            print(f">>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")
        
            #print(pag)
        # Agrega más opciones según sea necesario
        #print("pag: ", pag)
        
        #print("Boticas: ", boticas)

    for botica in boticas:
        print("Botica", botica.title)
        print("_" * 20)
        
        tag = botica.title
        
        categories = botica.get_categories()
        #print("all", categories)
        
        # Filtra para procesar solo una categoría, por ejemplo, la primera categoría
        filtered_categories = list(categories.items())[:2]
        #print("uno", filtered_categories)

        for category_url, category_title in filtered_categories:
            
            products_url = botica.get_product_urls(category_url)
            
            if not products_url:
                print(f"{tag} >>> Hubo un error en la categoria {category_title} - {category_url}")
                continue        
                   
            products_url = list(set(products_url))            
            # Error download products
            products_black_list = []
            
            # All Products
            products_internal_all = []
            
            # Fake MultiTasking
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(download_product, botica, product_url): product_url for product_url in products_url[:5]}
                for future in concurrent.futures.as_completed(futures):
                    try:
                        product_url, products_internal = future.result()
                        if products_internal: 
                            for product_internal in products_internal:
                                if isinstance(product_internal, Product):
                                    products_internal_all.append(product_internal)                   
                                
                        else:
                            products_black_list.append(product_url)  
                    except Exception as e:                
                            print(f"Hubo un error al descargar product -> {str(e)}") 
                
            
            if len(products_black_list) > 0:
                print(f"{tag} >>> Descargando productos de la Black List")
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = {executor.submit(download_product, botica, product_url): product_url for product_url in products_black_list}
                    for future in concurrent.futures.as_completed(futures):                                        
                        try:
                            product_url, products_internal = future.result()
                            if products_internal: 
                                for product_internal in products_internal:
                                    if isinstance(product_internal, Product):
                                        products_internal_all.append(product_internal)                  
                                        
                            else:
                                print(f"{tag} >>> Error al descargar -> black product {product_url}")
                            
                                
                        except Exception as e:                
                            print(f"Hubo un error al descargar black product -> {str(e)}") 
                
            
        chunk_size = 50
        simbol_concantened = "¬"
        chunks = np.array_split(products_internal_all, np.ceil(len(products_internal_all) / chunk_size))

        # Recorrer los trozos
        for chunk in chunks:
            product_texts = [product_internal.show_information() for product_internal in chunk]
                
            final_products_text = simbol_concantened.join(product_texts)            
            print(final_products_text)   
            #upload_to_db(final_products_text)
                        
      
        print("\n\n")
        
# Obtener las páginas disponibles
pags_farmacias = [
    {"name": "Botica Salud", "value": "https://www.boticasysalud.com/"},
    {"name": "Botica Peru", "value": "https://boticasperu.pe/"},
    {"name": "Hogar y Salud", "value": "https://www.hogarysalud.com.pe/"},
    {"name": "Farmacia Universal", "value": "https://farmaciauniversal.com/"},
    {"name": "Inkafarma", "value": "https://inkafarma.pe/"},
    {"name": "Mi Farma", "value": "https://www.mifarma.com.pe/"}
]

# Preguntar al usuario qué páginas quiere scrapear
questions = [
    inquirer.Checkbox('Farmacias',
                      message='Selecciona las paginas para el scraping:',
                      choices=pags_farmacias)
]
answers = inquirer.prompt(questions)

selected_pags = answers.get('Farmacias', [])

#print(selected_pags)
# Llamar a la función de scraping solo si se seleccionaron páginas
if selected_pags:
    scrape_selected_pages(selected_pags)
else:
    print("No se seleccionaron páginas para el scraping.")
