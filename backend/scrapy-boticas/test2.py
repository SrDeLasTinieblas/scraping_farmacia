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

def get_category_and_product_info(botica):
    categories = botica.get_categories()
    total_categories = len(categories)
    print(f"Tamaño de categorías en {botica.name}: {total_categories}")

    # Preguntar al usuario qué categorías quiere scrapear
    selected_categories = get_selected_categories(categories)
    
    total_products = 0
    inicio = time.time()

    #for category_url in tqdm(selected_categories, desc="Obteniendo productos", unit="categoría"):
    for category_url in selected_categories:
        total_products += len(botica.get_product_urls(category_url))

    print(f"Tamaño total de productos en {botica.name}: {total_products}")
    fin = time.time()
    tiempo_transcurrido = fin - inicio
    print(f">>> Tiempo transcurrido para obtener todos los URLs de productos es: {tiempo_transcurrido:.2f} segundos")

    return selected_categories, total_products

"""
def get_selected_categories(all_categories):
    questions = [
        inquirer.Checkbox('categories',
                          message='Selecciona las categorías para el scraping:',
                          choices=[(category.name, category) for category in all_categories])
    ]
    answers = inquirer.prompt(questions)
    selected_categories = answers.get('categories', [])
    return selected_categories
"""

def get_selected_categories(all_categories):
    questions = [
        inquirer.Checkbox('categories',
                          message='Selecciona las categorías para el scraping:',
                          choices=[(category["name"], category) for category in all_categories])
    ]
    answers = inquirer.prompt(questions)
    selected_categories = answers.get('categories', [])
    return selected_categories


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
        "https://www.hogarysalud.com.pe/": HogarSalud(),
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
            futures = [executor.submit(download_product, botica, product_url) for category_url in categories for product_url in botica.get_product_urls(category_url)]#[:2]]

            for future in concurrent.futures.as_completed(futures):
                product_url, products_internal = future.result()

                if products_internal:
                    products_internal_all.extend([product_internal for product_internal in products_internal if isinstance(product_internal, Product)])
                else:
                    products_black_list.append(product_url)

        chunk_size = 50
        simbol_concantened = "¬"
        chunks = np.array_split(products_internal_all, np.ceil(len(products_internal_all) / chunk_size))

        for chunk in chunks:
            product_texts = [product_internal.show_information() for product_internal in chunk]
            final_products_text = simbol_concantened.join(product_texts)
            final_products_text = f"{botica.id}¯{final_products_text}{simbol_concantened}"

            server = '154.53.44.5\SQLEXPRESS'
            database = 'BDCOMPRESOFT'
            username = 'userTecnofarma'
            password = 'Tecn0farm@3102'

            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
            try:
                with pyodbc.connect(conn_str) as conn:
                    cursor = conn.cursor()
                    cursor.execute("{CALL uspOperacionesMovimientosImportarFarmaciasCSV (?)}", (final_products_text))
                    print(final_products_text)
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                errormsg = ex.args[1]
                print(f"Error de SQL Server: SQLState - {sqlstate}, ErrorMessage - {errormsg}")

# Obtener las páginas disponibles
pages_with_categories = [
    Page(name="Botica Salud", value="https://www.boticasysalud.com/"),
    Page(name="Botica Peru", value="https://boticasperu.pe/"),
    Page(name="Hogar y Salud", value="https://www.hogarysalud.com.pe/"),
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