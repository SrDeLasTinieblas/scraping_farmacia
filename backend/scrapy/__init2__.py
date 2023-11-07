import random
import time
import requests
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures


inicio = time.time()
# Crear una instancia de la clase BoticasPeru
# Crear una instancia de la clase BoticasPeru
boticas_peru = BoticasPeru("Boticas Peru", "https://boticasperu.pe")
boticas_salud = BoticasSalud("Boticas y Salud", "https://www.boticasysalud.com")

categoriesSalud = boticas_salud.get_categories()

# Inicializa la lista de productos
products = []

# Inicializa un conjunto para mantener productos únicos
unique_products = set()

# Inicializa un conjunto para mantener categorías únicas
unique_categories = set()

# Inicializa un diccionario para mapear categorías a productos
category_products = {}
total_items = 0

def get_products_safely(categoria_url, retries=3):
    for _ in range(retries):
        try:
            return boticas_salud.get_all_products_in_category(categoria_url)
        except Exception as e:
            print(f"Error al obtener productos: {str(e)} {categoria_url}")
            time.sleep(5)  # Espera 5 segundos antes de volver a intentarlo
    return []

# Luego, en tu bucle principal
for category_url in categoriesSalud:
    last_segment = category_url.split('/')[-1]
    print(last_segment)
    category_products[last_segment] = get_products_safely(category_url)
    print(f"Obtenidos {len(category_products[last_segment])} productos de {category_url}")


count_categorias = 0
count_productos = 0

for category_name, products in category_products.items():
    count_categorias += 1
    print(f"Nombre de la categoría: {category_name}")
    print(f"Número de productos en la categoría: {len(products)}")
    print("Productos:")
    for product in products:
        count_productos += 1
        print("Nombre:", product.name)
        print("Presentación:", product.presentation)
        print("Marca:", product.brand)
        print("Precio por caja:", product.price_box)
        print("Precio blister:", product.price_blister)
        print("Fuente de Información:", product.source_information)
        print("Lifting Date:", product.lifting_date)
        print("Laboratorio:", product.laboratory)
        print("Card Discount:", product.card_discount)
        print("Crossed Price:", product.crossed_price)
        print("Suggested Comment:", product.suggested_comment)
        print("\n")  # Agrega una línea en blanco entre productos

print(f"Total de productos en todas las categorías: {count_productos}")
print(f"Total de categorías: {count_categorias}")


'''
for product in unique_products:
    count +=1
    print("Nombre:", product.name)
    print("Presentación:", product.presentation)
    print("Marca:", product.brand)
    print("Precio por caja:", product.price_box)
    print("Precio blister:", product.price_blister)
    print("Fuente de Información:", product.source_information)
    print("Lifting Date:", product.lifting_date)
    print("Laboratorio:", product.laboratory)
    print("Card Discount:", product.card_discount)
    print("Crossed Price:", product.crossed_price)
    print("Suggested Comment:", product.suggested_comment)
    print("\n")  # Agrega una línea en blanco entre productos
'''

fin = time.time()
tiempo_transcurrido = fin - inicio
print(f'Tiempo transcurrido de Obtener todos los urls products es : {tiempo_transcurrido:.2f} segundos')


final_products_url = []
categories_black_list = []
products_black_list = []

'''


url = "https://bys-prod-backend.azurewebsites.net/api/ServiceProduct?filterValue=1-primerosauxilios&filterBy=2&CurrentPage=4&PageSize=12"
        
user_agent = get_random_user_agent()
my_headers = {
            "User-Agent": user_agent            
        }

payload = {}

response = requests.request("GET", url, headers=my_headers, data=payload)

print("Response ::> ", response.text)
print(f"mi User Agent: {my_headers}")



'''









