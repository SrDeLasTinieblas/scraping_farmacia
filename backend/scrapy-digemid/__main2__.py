import random
from time import time
import traceback
from pages.Digemid import Digemid
from utils.UploadDatabase import upload_to_db
import pyodbc

"""
    Farmacia Universal  = 1
    Inkafarma           = 2
    Boticas y Salud     = 3
    Boticas Peru        = 4
    Hogar y Salud       = 5
    Digemin             = 6
    
"""


def chunks(lst, chunk_size):
    """Divide la lista en bloques del tamaño especificado."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def connect_to_database(server, database, username, password):
    """Establece la conexión a la base de datos."""
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return conn, cursor

def upload_to_db(cursor, text_upload):
    """Sube productos a la base de datos."""
    try:
        cursor.execute("{CALL uspOperacionesMovimientosImportarDIGEMIDCSV (?)}", (text_upload))
        cursor.commit()
        return True 
    except Exception as e:
        print(f"Error al cargar en la base de datos: {str(e)}")
        traceback.print_exc()
        return False
    
    
    
    
def upload_to_db_bulk_transaction(cursor, products):
    """Sube productos a la base de datos en bloques usando transacción."""
    try:
        cursor.execute("BEGIN TRANSACTION;")

        # Asegúrate de que el tipo de datos coincida con el procedimiento almacenado
        cursor.executemany("{CALL uspOperacionesMovimientosImportarDIGEMIDCSV (?)}", [(str(product[0]),) for product in products])

        cursor.execute("COMMIT;")
        return True 
    except Exception as e:
        print(f"Error al cargar en la base de datos: {str(e)}")
        traceback.print_exc()
        cursor.execute("ROLLBACK;")
        return False


    


def main():
    digemid = Digemid()
    simbol_concantened = "¬"
    total_productos_enviados = 0  
    resultados = digemid.obtenerParametros()
    products_digimid = []
    tiempo_inicial = time()
    nombre_de_product = ""

    print("Tamaño de productos a obtener:", len(resultados))

    if len(resultados) > 0:
        for resultado in resultados:
            print(f"resultado -><- {resultado}")
            nombre_de_product = resultado['PROD_NOMBRE']
            concentracion = resultado['PROD_CONCENTRACION']
            
            key_productos = digemid.step_2(product_name=nombre_de_product, product_concent=concentracion)
            if not key_productos:
                continue
            
            for key_producto in key_productos:
                key_grupo = key_producto["grupo"]
                key_concent = key_producto["concent"]
                key_codGrupoFF = key_producto["codGrupoFF"]  

                products = digemid.step_3(key_group=key_grupo, 
                                        key_concent=key_concent,
                                        nombre_producto=nombre_de_product,
                                        key_codGrupoFF=key_codGrupoFF
                                    )
                if not products:
                    continue
                
                for product in products:
                    if not product:
                        continue
                    
                    internal_product = digemid.step_4(product)            
                    if not internal_product:
                        continue
                    products_digimid.append(internal_product)
                
    products_text = [product.show_information() for product in products_digimid]
    final_products_text = simbol_concantened.join(products_text)
    final_products_text_with_prefix = f"6¯{final_products_text}"

    total_productos_enviados = len(products_digimid)

    # Conectar a la base de datos
    server = '154.53.44.5\SQLEXPRESS'
    database = 'BDCOMPRESOFT'
    username = 'userTecnofarma'
    password = 'Tecn0farm@3102'
    
    conn, cursor = connect_to_database(server, database, username, password)

    
    product_chunks = list(chunks(products_digimid, 50))

    count = 0
    for chunk in product_chunks:
        final_products_text = simbol_concantened.join([product.show_information() for product in chunk])
        final_products_text_with_prefix = f"6¯{final_products_text}"

        #products_to_upload = [(final_products_text_with_prefix,) for _ in chunk]

        count += 1
        upload_to_db(cursor, final_products_text_with_prefix)
        #upload_to_db_bulk_transaction(cursor, products_to_upload)

        with open(f"product_chunks {count}.txt", "w", encoding="utf-8") as file:
            file.write(final_products_text_with_prefix + "\n")

    print(f"Total de productos enviados al final: {total_productos_enviados}")
    tiempo_final = time()
    tiempo_total = tiempo_final - tiempo_inicial
    print("Tiempo total de ejecución: {} segundos".format(tiempo_total))

    
    conn.close()

if __name__ == "__main__":
    main()
    

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




