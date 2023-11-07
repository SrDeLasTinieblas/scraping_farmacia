import random
import time
from pages.BoticasPeru import BoticasPeru
from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures

inicio = time.time()

# Crear una instancia de la clase BoticasPeru
boticas_peru = BoticasPeru("Boticas Peru", "https://boticasperu.pe")

# Obtener la lista de categorías
categories = boticas_peru.get_categories()
#categories = categories[:1] --FOR ACTION


def download_product(product_url):
    print("Descargando product ", product_url)
    return product_url, boticas_peru.get_product(product_url)


final_products_url = []
categories_black_list = []
products_black_list = []


for category_url in categories:
    
    # Ejemplo de category_url
    # https://boticasperu.pe/promociones.html
    conter = 0
    is_equals = True
    lastest_product_urls_hash = None
    
    category_products_url = []   
       
    while is_equals:
        conter += 1
        # https://boticasperu.pe/promociones.html?p=1
        final_category_url =  f"{category_url}?p={conter}"
        print(f"Pag :: {final_category_url}")
        product_urls = boticas_peru.get_product_urls(final_category_url)
        
        if not product_urls:
            categories_black_list.append(final_category_url)
            continue
                    
        for product_url in product_urls:
            final_products_url.append(product_url)                  
            category_products_url.append(product_url)                 

        
        my_tuple = tuple(product_urls) 
        hash_tuple = hash(my_tuple)
        
        if lastest_product_urls_hash == hash_tuple:
            is_equals = False
        else:
            lastest_product_urls_hash = hash_tuple       

    category_products_size = len(category_products_url)
    products_url_size = len(final_products_url)
    print(f"Cantidad de Products en Categoria :: {category_url} -> Tamaño :: {category_products_size}")



products_url_size = len(final_products_url)
print(f"Cantidad de Products Final :: {products_url_size}")

fin = time.time()
tiempo_transcurrido = fin - inicio
print(f'Tiempo transcurrido de Obtener todos los urls products es : {tiempo_transcurrido:.2f} segundos')


if len(categories_black_list) > 0:
    print(f"Descargando nuevamente Categories de Black List")
    for category_black in categories_black_list:
        print(f"Descargando Bkack Category : {category_black}")
        product_urls = boticas_peru.get_product_urls(category_black)
        
        if not product_urls:
            print(f"Productos nos descargados de black category {category_black}")
            continue
                    
        for product_url in product_urls:
            final_products_url.append(product_url)                  
        


print("Descargando Productos ....")

unique_products_url = list(set(final_products_url))
# unique_products_url = unique_products_url[:10] --FOR ACTION

threaded_start = time.time()
products = []

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for url in unique_products_url:
        futures.append(executor.submit(download_product, product_url=url))
    for future in concurrent.futures.as_completed(futures):
        product_url, product = future.result()
        if product:
           products.append(product)
        else:
            products_black_list.append(product_url)


if len(products_black_list) > 0:
    print("Descargando products de la Black List")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for url in products_black_list:
            futures.append(executor.submit(download_product, product_url=url))
        for future in concurrent.futures.as_completed(futures):
            product_url, product = future.result()
            if product:
                products.append(product)
            else:
                print(f"Error al descargar -> black product {product_url}")


print("Descarga de productos finalizado : ", time.time() - threaded_start)

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

    
"""

##
# Contador para limitar a 10 ejecuciones
#execution_count = [0]

def process_category(category_url):
    #if execution_count[0] >= 10:
     #   return  # No hacer nada si ya se han realizado 10 ejecuciones
    
    print("Categoría:", category_url)

    # Obtener los productos para la categoría actual
    products = boticas_peru.get_product_urls(category_url)
    
    # Iterar sobre cada producto
    for random_product_url in products:
 #       if execution_count[0] >= 10:
  #          return  # No hacer nada si ya se han realizado 10 ejecuciones
        
        product = boticas_peru.get_product(random_product_url)
        print("Product:", product)
        print("-" * 10)

   #     execution_count[0] += 1  # Incrementar el contador

# Utilizar ThreadPoolExecutor para ejecutar en paralelo
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Ejecutar la función process_category para cada categoría en paralelo
    results = executor.map(process_category, categories)

"""



# Recorrer las categorías y obtener los productos
"""
    En las Categories Url para mas productos se puede poner al final ?p=2
    Ejemplo: https://boticasperu.pe/promociones.html?p=3

"""

"""
for category_url in category_urls:
    product_urls = boticasPeru.get_product_urls(category_url)
        
    print(f"Categoría: {category_url}")
    print("\tProductos:")
    
    for product_url in product_urls:
        print("\t\t"+product_url)        
        product = boticasPeru.get_product(product_url)


random_category_url = random.choice(categories)   
random_product_url = random.choice(boticas_peru.get_product_urls(random_category_url)) 
#random_product_url = "https://boticasperu.pe/atorvastatina-20-mg-tabletas-recubiertas-caja-100-un.html" 

product = boticas_peru.get_product(random_product_url)
product.show_information()
   
"""   