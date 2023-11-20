import random
import time
from pages.FarmaUniversal import FarmaUniversal
from pages.Inkafarma import Inkafarma
from pages.BoticasSalud import BoticasSalud
from pages.BoticasPeru import BoticasPeru
from pages.HogarSalud import HogarSalud
from pages.MiFarmaX import MiFarma
from pages.Digemid import Digemid
from model.Models import Product
from utils.NetUtils import download_page, get_random_user_agent
import concurrent.futures
from utils.UploadDatabase import upload_to_db

"""
    Farmacia Universal  = 1
    Inkafarma           = 2
    Boticas y Salud     = 3
    Boticas Peru        = 4
    Hogar y Salud       = 5
    Digemin             = 6
    
"""

digemid = Digemid()


categories = digemid.get_categories()
simbol_concantened = "¬"
products_information_list = []
min_required_products = 5

print(categories)

# Continuar hasta que se obtengan al menos 5 productos
while len(products_information_list) < min_required_products:
    # Recorrer cada categoría y obtener información de productos
    for category in categories:
        product_ids = digemid.get_product_urls(category)
        for product_id in product_ids:#[:1]:
            products = digemid.get_product(product_id)
            if len(products) >= 1:
                print("Tamaño: ", len(products))
                print("product_id: ", len(product_id))
                for product in products:
                    product_more_details = digemid.get_product_more_details(product)
                    if not product_more_details:
                        continue
                    # Cambié 'show_information' a 'show_information2' para que coincida con tu código anterior
                    product_information = product_more_details.show_information()
                    
                    # Verificar si la información del producto no es None antes de agregarla a la lista
                    if product_information is not None:
                        products_information_list.append(product_information)
                    else:
                        print("La información del producto es None. Intentando otro producto.")

# Dividir la lista en trozos de 50 productos
chunk_size = 50
chunks = [products_information_list[i:i+chunk_size] for i in range(0, len(products_information_list), chunk_size)]

# Iterar sobre los trozos y enviar a la base de datos
for chunk in chunks:
    # Unir la lista de información de productos con el símbolo 'simbol_concantened'
    final_products_text = simbol_concantened.join(map(str, chunk))
    final_products_text = f"{digemid.id}¯{final_products_text}{simbol_concantened}"
    print(final_products_text)
    # upload_to_db(final_products_text)  # Descomenta esta línea cuando estés listo para enviar a la base de datos


            
"""            
for category in categories:
    product_ids = digemid.get_product_urls(category)

    for product_id in product_ids[:5]:
        products = digemid.get_product(product_id)

        # Verificar si 'products' es None o no es iterable
        if products is None or not isinstance(products, (list, tuple)):
            print(f"Hubo un error al obtener productos para el ID {product_id}")
            continue

        for product in products:
            product_more_detais = digemid.get_product_more_details(product)

            if not product_more_detais:
                continue

            final_products_text = simbol_concantened.join(product_more_detais)
            final_products_text = f"{digemid.id}¯{final_products_text}{simbol_concantened}"
            print(final_products_text)
            upload_to_db(final_products_text)
                    For next call need data
                    codigoProducto":53725,"         ====> codProdE  ====> name
                    codEstablecimiento":"0053974"   ====> codEstab  ====> id_sku
                
      
# For More Datails :V

product = Product(
    id_sku = "0022645",
    name =  53725,
    presentation =  None,
    brand = None,
    price =  None,
    source_information = None,
    lifting_date =  None,
    laboratory =  None,
    card_discount = None,
    crossed_price =  None,
    suggested_comment =  None,
    description=None
)

product_more_detais = digemid.get_product_more_details(product)
#product_more_detais.show_information2()
#print(product_more_detais)
"""




