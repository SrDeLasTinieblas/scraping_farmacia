import concurrent.futures
import traceback
import numpy as np

from model.Models import Product

from pages.FarmaUniversal import FarmaUniversal
from pages.Inkafarma import Inkafarma
from pages.MiFarmaX import MiFarma
from pages.BoticasSalud import BoticasSalud
from pages.BoticasPeru import BoticasPeru
from pages.HogarSalud import HogarSalud

from utils.UploadDatabase import upload_to_db

boticas = [
    #BoticasPeru(),      # si envia  ---
    #BoticasSalud(),    # si envia  ---
    #HogarSalud(),       # si envia ---
    #FarmaUniversal(),  # si envia  ---
    Inkafarma()        # si envia
    
    #MiFarma()
]

'''
def download_product(botica, product_url):
    tag = botica.title 
    print(f"{tag} >>> Descargando producto ", product_url)
    return product_url, botica.get_product(product_url)

def retry_download(botica, products_black_list):
    print(f"{botica.title} >>> Descargando productos de la Black List")
    products_internal_all = []

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
                    print(f"{botica.title} >>> Error al descargar -> black product {product_url}")
            except Exception as e:                
                print(f"Hubo un error al descargar black product -> {str(e)}")
                traceback.print_exc()

    return products_internal_all


def main():
    for botica in boticas:
        print("Botica", botica.title)
        print("_" * 20)

        tag = botica.title

        categories = botica.get_categories()
        for category_url, category_title in list(categories.items()):
            print(tag, ">>>> ",category_title, ":", category_url)

            products_url = botica.get_product_urls(category_url)

            if not products_url:
                print(f"{tag} >>> Hubo un error en la categoria {category_title} - {category_url}")
                continue        

            products_url = list(set(products_url))            
            products_black_list = []

            # All Products
            products_internal_all = []

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(download_product, botica, product_url): product_url for product_url in products_url}
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
                        traceback.print_exc()

            # Retry failed downloads
            if len(products_black_list) > 0:
                products_internal_all += retry_download(botica, products_black_list)

            # Count and print downloaded products
            print(f"{botica.title} >>> Total de productos descargados: {len(products_internal_all)}")
            
    chunk_size = 50
    simbol_concantened = "¬"
    chunks = np.array_split(products_internal_all, np.ceil(len(products_internal_all) / chunk_size))

    # Recorrer los trozos
    for chunk in chunks:
        product_texts = [product_internal.show_information() for product_internal in chunk]
        
        final_products_text = simbol_concantened.join(product_texts)
        final_products_text = f"{botica.id}¯{final_products_text}{simbol_concantened}"
        print(final_products_text)       
        #upload_to_db(final_products_text)

if __name__ == "__main__":
    main()
'''
    

def download_product(botica, product_url):
    tag = botica.title 
    print(f"{tag} >>> Descargando producto ", product_url)
    return product_url, botica.get_product(product_url)


for botica in boticas:
    print("Botica", botica.title)
    print("_" * 20)
    
    tag = botica.title
    
    categories = botica.get_categories()
    #print("categories", categories)
    for category_url, category_title in list(categories.items()):
    #for category_url, category_title in list(categories.items()):
        #print(tag, ">>>> ",category_title, ":", category_url)
        
        products_url = botica.get_product_urls(category_url)
        
        if not products_url:
            #print(f"{tag} >>> Hubo un error en la categoria {category_title} - {category_url}")
            continue        
               
        products_url = list(set(products_url))            
        # Error download products
        products_black_list = []
        
        # All Products
        products_internal_all = []
        
        # Fack MultiTasking
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(download_product, botica, product_url): product_url for product_url in products_url}#[:10]}
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
            final_products_text = f"{botica.id}¯{final_products_text}{simbol_concantened}"
            print(final_products_text)       
            upload_to_db(final_products_text)
                    
  
    print("\n\n")
    
    
