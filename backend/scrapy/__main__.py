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

#digemid = Digemid()
#resultados = digemid.obtenerParametros()


#print(resultados)


digemid = Digemid()


simbol_concantened = "¬"
products_information_list = []
min_required_products = 5

products_to_send = 50 


resultados = digemid.obtenerParametros()

products_digimid = []

for resultado in resultados:
    #print(f"resultado -><- {resultado}")
    nombre_de_product = resultado['PROD_NOMBRE']
    departamento_id = resultado['IDDPTO']                 
    provincia_id = resultado['IDPROV']
    distrito_id = resultado['IDDIST']
    ubigeo_id = f"{departamento_id}{provincia_id}{distrito_id}"
    concentracion = resultado['PROD_CONCENTRACION']
    
    key_productos = digemid.step_2(product_name=nombre_de_product, product_concent=concentracion)
    if not key_productos:
        continue
    
    for key_producto in key_productos:
        #print(f"key_producto ->>>> {key_producto}")
        key_grupo = key_producto["grupo"]
        key_concent = key_producto["concent"]
        key_codGrupoFF = key_producto["codGrupoFF"]         

        products = digemid.step_3(key_group=key_grupo, 
                                 key_concent = key_concent,
                                 key_codGrupoFF = key_codGrupoFF,
                                 departament_id = departamento_id,
                                 province_id = provincia_id,
                                 ubigeo_id= ubigeo_id
                            )
        if not products:
            continue
        
        for product in products:
            if not product:
                continue
            
            internal_product = digemid.step_4(product)            
            if not internal_product:
                print(f"error en internal_products")
                continue
            products_digimid.append(internal_product)
            #internal_product.show_information2()
            #print(internal_product.show_information()) 
            #print("\n")  
            

# Número deseado de elementos por sublista
elementos_por_sublista = products_to_send
# Divide la lista en sublistas de 50 elementos
sublistas = [products_digimid[i:i+elementos_por_sublista] for i in range(0, len(products_digimid), elementos_por_sublista)]

# Imprime o utiliza las sublistas según tus necesidades
# Esto es cada 50
for i, sublista in enumerate(sublistas):
    products_text = []
    for product in sublista:
        products_text.append(product.show_information())    
    
    final_products_text = simbol_concantened.join(products_text)
    final_products_text = f"{digemid.id}¯{final_products_text}"
    # Enviar a Sensei
    print(final_products_text)   

     
     

"""
while True:
    # Recorrer cada categoría y obtener información de productos
    for category in categories:
        product_ids = digemid.get_product_urls(category)
        # Iterar sobre los product_ids y obtener los productos
        for product_id in product_ids:
            products = digemid.get_product(product_id)

            # Verificar si se descargaron productos correctamente
            if products:
                print(f"Se descargaron {len(products)} productos para el ID: {product_id}")
                # Puedes hacer más cosas con la lista de productos si es necesario
            #else:
                #print(f"No se descargaron productos para el ID: {product_id}")
                
            if products is not None and len(products) >= 1:
                print("Tamaño: ", len(products))
                print("product_id: ", len(product_id))
                for product in products:
                    product_more_details = digemid.get_product_more_details(product)
                    if not product_more_details:
                        continue

                    product_information = product_more_details.show_information()

                    # Verificar si la información del producto no es None antes de agregarla a la lista
                    if product_information is not None:
                        products_information_list.append(product_information)
                        products_collected += 1

                        # Verificar si se han recolectado 1000 productos
                        if products_collected % 20 == 0:
                            # Enviar productos a la base de datos en lotes de 50
                            chunks = [products_information_list[i:i + products_to_send] for i in
                                      range(0, len(products_information_list), products_to_send)]

                            for chunk in chunks:
                                final_products_text = simbol_concantened.join(map(str, chunk))
                                final_products_text = f"{digemid.id}¯{final_products_text}{simbol_concantened}"
                                print(final_products_text)
                                upload_to_db(final_products_text)  # Descomenta esta línea cuando estés listo para enviar a la base de datos

                            # Limpiar la lista después de enviar los productos
                            products_information_list = []

# Fin del bucle
"""
 

            
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




