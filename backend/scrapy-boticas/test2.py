import inquirer
from pages.base.base import Page
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
import pyodbc
#from tqdm import tqdm  # Importa la función tqdm
from colorama import Fore

def print_error(message):
    print(f"{Fore.RED}Error: {message}{Fore.RESET}")

def print_success(message):
    print(f"{Fore.GREEN}Success: {message}{Fore.RESET}")

def get_category_and_product_info(botica):
    categories = botica.get_categories()
    total_categories = len(categories)
    print(f"Tamaño de categorías en {botica.name}: {total_categories}")
    
    #if botica.name == 'Farmacia Universal':
      #  selected_categories_boticas_universal = get_selected_categories(categories, lambda category: category.name)
    #if botica.name == 'Inkafarma':
     #   selected_categories_inkafarma = get_selected_categories(categories, lambda category: category["name"])

    # Preguntar al usuario qué categorías quiere scrapear
    selected_categories = get_selected_categories(categories)
    
    total_products = 0
    inicio = time.time()

    #for category_url in tqdm(selected_categories, desc="Obteniendo productos", unit="categoría"):
    for category_url in selected_categories:
        #print("category_url: ", category_url)
        total_products += len(botica.get_product_urls(category_url))

    print(f"Tamaño total de productos en {botica.name}: {total_products}")
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f">>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")

    return selected_categories, total_products


def get_selected_categories(all_categories):
    questions = [
        inquirer.Checkbox('categories',
                          message='Selecciona las categorías para el scraping:',
                          choices=[(category["name"], category) for category in all_categories])
    ]
    answers = inquirer.prompt(questions)
    selected_categories = answers.get('categories', [])
    return selected_categories


# Uso para Boticas Universal
#selected_categories_boticas_universal = get_selected_categories(all_categories_boticas_universal, lambda category: category.name)

# Uso para Inkafarma
#selected_categories_inkafarma = get_selected_categories(all_categories_inkafarma, lambda category: category["name"])


"""


def get_selected_categories(all_categories, map_function):
    questions = [
        inquirer.Checkbox('categories',
                          message='Selecciona las categorías para el scraping:',
                          choices=[(map_function(category), category) for category in all_categories])
    ]
    answers = inquirer.prompt(questions)
    selected_categories = answers.get('categories', [])
    return selected_categories
    

def get_selected_categories(all_categories):
    questions = [
        inquirer.Checkbox('categories',
                          message='Selecciona las categorías para el scraping:',
                          choices=[(category.name, category) for category in all_categories])
    ]
    answers = inquirer.prompt(questions)
    selected_categories = answers.get('categories', [])
    return selected_categories


def get_selected_categories(all_categories):
    questions = [
        inquirer.Checkbox('categories',
                          message='Selecciona las categorías para el scraping:',
                          choices=[(category["name"], category) for category in all_categories])
    ]
    answers = inquirer.prompt(questions)
    selected_categories = answers.get('categories', [])
    return selected_categories
"""

def download_product(botica, product_url):
    try:
        return product_url, botica.get_product(product_url)
    except Exception as e:
        print(f"Hubo un error al descargar producto de {botica.name} -> {str(e)}")
        return None, None

def scrape_selected_pages(selected_pags):
    boticas_instances = {
        "https://www.boticasysalud.com/": BoticasSalud(),
        "https://boticasperu.pe/": BoticasPeru(),
        "https://www.hogarysalud.com.pe": HogarSalud(),
        "https://farmaciauniversal.com/": FarmaUniversal(),
        "https://inkafarma.pe/": Inkafarma(),
        # Agrega más instancias según sea necesario
    }

    boticas = []

    for pag in selected_pags:
        botica_instance = boticas_instances.get(pag.value)
        if botica_instance:
            categories, total_products = get_category_and_product_info(botica_instance)
            boticas.append((botica_instance, total_products, categories))

    for botica, total_products, categories in boticas:
        print("_" * 20)
        print(f"Botica: {botica.name}")

        products_internal_all = []
        products_black_list = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(download_product, botica, product_url) for category_url in categories for product_url in botica.get_product_urls(category_url)]

            for future in concurrent.futures.as_completed(futures):
                product_url, products_internal = future.result()

                if products_internal:
                    products_internal_all.extend([product_internal for product_internal in products_internal if isinstance(product_internal, Product)])
                else:
                    products_black_list.append(product_url)

        chunk_size = 500
        simbol_concantened = "¬"
        chunks = np.array_split(products_internal_all, np.ceil(len(products_internal_all) / chunk_size))

        count = 0
        # Recorrer los trozos
        for chunk in chunks:
            product_texts = [product_internal.show_information() for product_internal in chunk]
            
            final_products_text = simbol_concantened.join(product_texts)
            final_products_text = f"{botica.id}¯{final_products_text}" #{simbol_concantened}"
            count +=1
            
            try:
                upload_to_db(final_products_text)
                with open(f"Output{count}.txt", "w") as text_file:
                    text_file.write(products_internal_all)
                    
                print_success(f"{count} Lote subido exitosamente.")
            except Exception as e:
                print_error(f"Error al subir el lote: {str(e)}")
            
            #upload_to_db(final_products_text)
            print(final_products_text)
    print(f"\nTamaño total de productos subidos: {len(products_internal_all)}")
    


# Obtener las páginas disponibles
pages_with_categories = [
    Page(name="Botica Salud", value="https://www.boticasysalud.com/"),
    Page(name="Botica Peru", value="https://boticasperu.pe/"),
    Page(name="Hogar y Salud", value="https://www.hogarysalud.com.pe"),
    Page(name="Farmacia Universal", value="https://farmaciauniversal.com/"),
    Page(name="Inkafarma", value="https://inkafarma.pe/"),
    # Agrega más instancias según sea necesario
]


# Preguntar al usuario qué páginas quiere scrapear con categorías
questions = [
    inquirer.Checkbox('pages',
                      message='Selecciona las páginas para el scraping:',
                      choices=[(page.name, page) for page in pages_with_categories])
]
answers = inquirer.prompt(questions)

selected_pages = answers.get('pages', [])

# Llamar a la función de scraping solo si se seleccionaron páginas
if selected_pages:
    scrape_selected_pages(selected_pages)
else:
    print("No se seleccionaron páginas para el scraping.")