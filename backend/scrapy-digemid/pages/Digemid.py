import json
import traceback
from model.Models import ProductDigimid, Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_json, download_page
from utils.Utils import unique_text, decode_base64, hyphenated_string_to_tuple, tuple_to_hyphenated_string
import pyodbc


class Digemid(Page):
    
    def __init__(self, id = 6, title = "Digemid", url = "https://opm-digemid.minsa.gob.pe"):
        super().__init__(id, title, url)
        
    
    # Paso 2 Autocompletado, hay que buscar :()
    def step_2(self, product_name, product_concent):
        """
        The `step_2` function takes a product name and concentration as input, sends a POST request to a
        specific URL with the payload containing the search parameters, and returns a list of key products
        that match the given concentration.
        
        :param product_name: The product_name parameter is the name of the product you want to search for
        :param product_concent: The parameter "product_concent" represents the concentration of the product.
        It is used in the "step_2" function to filter the search results based on the concentration of the
        product
        :return: The function `step_2` returns a list of dictionaries containing information about the
        products that match the given `product_name` and `product_concent`. Each dictionary in the list
        represents a product and includes the following keys: "grupo", "concent", and "codGrupoFF".
        """
        search_word = product_name  
        #print("search word: ", search_word)
        url_post = "https://ms-opm.minsa.gob.pe/msopmcovid/producto/autocompleteciudadano"
        payload = json.dumps({
        "filtro": {
            "nombreProducto": f"{search_word}",
            "pagina": 1,
            "tamanio": 10,
            "tokenGoogle": ""
        }
        })
        
        # base url = https://opm-digemid.minsa.gob.pe
        # User-Agent
	
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': f"{self.url}",
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': f"{self.url}/",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }
        
        response_json = download_json(url =url_post, method="POST", headers=headers, data=payload)
        if not response_json:
           print(f"step_2 repsonse json null")
           return None
        
        data = response_json["data"]
        if not data:
           print(f"step_2 repsonse not data")
           return None
            
        key_products = {}        
            
        # Fix Made Fack
        product_concent = product_concent.replace(" ", "")    
        for item in data:                
            grupo = item["grupo"]
            concent = item["concent"]
            codGrupoFF = item["codGrupoFF"] 
            
            if product_concent == concent:
                key_product = {
                    "grupo": grupo,
                    "concent" : concent,
                    "codGrupoFF" : codGrupoFF 
                }
                key_products[f"{grupo}{concent}{codGrupoFF}"] = key_product
        
        key_products_list = key_products.values()
        key_products_list = list(key_products_list)
        return key_products_list          
            
         
    
    def obtenerParametros(self):
        """
        The function `obtenerParametros` connects to a SQL Server database, executes a stored procedure,
        retrieves the results as a list of dictionaries, and returns the results.
        :return: the results obtained from executing the stored procedure
        "uspOperacionesConsultaDigemidItems" in the database. The results are returned as a list of
        dictionaries, where each dictionary represents a row in the result set.
        """

        server = '154.53.44.5\SQLEXPRESS'
        database = 'BDCOMPRESOFT'
        username = 'userTecnofarma'
        password = 'Tecn0farm@3102'
    
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        resultados = []

        try:
            # Ejecuta el procedimiento almacenado
            cursor.execute("EXEC uspOperacionesConsultaDigemidItems")

            # Obtiene los nombres de las columnas
            column_names = [column[0] for column in cursor.description]

            # Obtiene los resultados como una lista de diccionarios
            resultados = [dict(zip(column_names, row)) for row in cursor.fetchall()]

            # for resultado in resultados:
            #    print("==>" + resultado)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Cierra el cursor y la conexión
            cursor.close()
            conn.close()

        return resultados
           
              
    # Paso 3                        
    def step_3(self, key_group, key_concent,nombre_producto, key_codGrupoFF):   
        """
        The function `step_3` takes in several parameters, makes a POST
        request to a specific URL with the given payload, and extracts data
        from the response to create a list of Product objects.
        
        :param key_group: The key_group parameter is used to specify the code
        of the product group. It is expected to be an integer value
        :param key_concent: The parameter "key_concent" is used to specify the
        concentration of the product. It is a key that represents the
        concentration value of the product
        :param key_codGrupoFF: The parameter "key_codGrupoFF" is used to
        specify the code of the product group. It is used in the API request
        to filter the products based on their group
        :param departament_id: The `departament_id` parameter represents the
        code for the department (or region) where the product is being
        searched for. It is used to filter the search results based on the
        specified department
        :param province_id: The parameter "province_id" is used to specify the
        code of the province for which you want to retrieve data. It is used
        in the API request to filter the results based on the specified
        province
        :param ubigeo_id: The `ubigeo_id` parameter is used to specify the
        code for a specific location in Peru. It is a unique identifier for a
        geographical area and is used to filter the search results for
        products in that particular location
        :return: a list of Product objects.
        """     
        product_code = key_group
        concent = key_concent
        codGrupoFF = key_codGrupoFF
        
        product_code = int(product_code)
        url_post = "https://ms-opm.minsa.gob.pe/msopmcovid/preciovista/ciudadano"

        payload = json.dumps({
        "filtro": {
                "codigoProducto": product_code,
                "codigoDepartamento": None,
                "codigoProvincia": None,
                "codigoUbigeo": None,
                "codTipoEstablecimiento": None,
                "catEstablecimiento": None,
                "nombreEstablecimiento": None,
                "nombreLaboratorio": None,
                "codGrupoFF": f"{codGrupoFF}",
                "concent": f"{concent}",
                "tamanio": 10,
                "pagina": 1,
                "tokenGoogle": "SiniurDeveloper",
                "nombreProducto": f"{nombre_producto}"
            }
        })
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': f"{self.url}",
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': f"{self.url}/",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }

        response_json = download_json(method="POST", url=url_post, headers=headers, data=payload)
        
        
        if not response_json:
            print(f"{self.title} : Hubo un error al descargar el producto")
            return None         
        
        data = response_json["data"]
        if not data:
            #print(f"{self.title} : Hubo un error al obtener [data] en el producto {key_group}")
            return None
        
        products_dic = {}   
        products = []
        
        try:
            for item in data:
                #print(f"\nitem ----> {item}\n")
            
                codEstab = item["codEstab"]
                codProdE = item["codProdE"]
                
                #precio2 = item["precio2"]
                #precio3 = item["precio3"]
                
                # 3.9
                precio = item["precio1"]
                
                # Solución Oral
                nombreFormaFarmaceutica = item["nombreFormaFarmaceutica"]
                
                # 120 mg/ 5 mL\t
                concent = item["concent"]
                
                # PARACETAMOL
                nombreProducto = item["nombreProducto"]
                
                # BOTICAS Y SALUD
                nombreComercial = item["nombreComercial"]

                # LABORATORIOS PORTUGAL S.R.L.
                nombreLaboratorio = item["nombreLaboratorio"]
                
                product_id = unique_text(
                    nombreProducto, 
                    concent,
                    nombreFormaFarmaceutica,
                    nombreComercial,
                    nombreLaboratorio, 
                    precio
                )
                
                
                products_dic[product_id] = Product(
                    id_sku = codEstab,
                    name =  codProdE,
                    presentation =  concent,
                    brand = None,
                    price = f"{float(precio):.2f}" if f"{float(precio):.2f}" else None,
                    source_information =  self.title,
                    lifting_date =  None,
                    laboratory =  nombreLaboratorio,
                    #card_discount =  f"Precio con todas las tarjetas: {price_with_payment_method} Precio Monedero del Ahorro: {price_all_payment_method}",
                    card_discount = None,
                    crossed_price =  None,
                    suggested_comment =  None,
                    description=None
                )

                """
                    For next call need data
                    codigoProducto":53725,"         ====> codProdE  ====> name
                    codEstablecimiento":"0053974"   ====> codEstab  ====> id_sku
                """
        
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en ->Nombre del producto: {nombreProducto}: {str(e)}")   
            return None
        

        for key, product in products_dic.items():    
            products.append(product)      
    
    
        return products if products else None
    
    def step_4(self, product):
        """
            For next call need data
            codigoProducto":53725,"         ====> codProdE  ====> name
            codEstablecimiento":"0053974"   ====> codEstab  ====> id_sku
        """
        codigoProducto = int(product.name)
        codEstablecimiento = f"{product.id_sku}" 
        key_concent = f"{product.presentation}" 
        
        url_post = "https://ms-opm.minsa.gob.pe/msopmcovid/precioproducto/obtener"

        payload = json.dumps({
        "filtro": {
            "codigoProducto": codigoProducto,
            "codEstablecimiento": codEstablecimiento,
            "tokenGoogle": ""
        }
        })
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': f"{self.url}",
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': f"{self.url}/",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }

        response_json = download_json(method="POST", url = url_post, headers=headers, data=payload)
        
        if not response_json:
            print("response_json is None")
            return None

        #print(f"response_json {response_json}")                
        entity = response_json.get("entidad")
        
        if not entity:
            #print("entity is None")
            return None
        
        
        try:           
            precio1 = entity.get("precio1")
            precio2 = entity.get("precio2")
            nombreProducto = entity.get("nombreProducto")
            paisFabricacion = entity.get("paisFabricacion")
            registroSanitario = entity.get("registroSanitario")
            condicionVenta = entity.get("condicionVenta")
            tipoProducto = entity.get("tipoProducto")
            nombreTitular = entity.get("nombreTitular")
            nombreFabricante = entity.get("nombreFabricante")
            presentacion = entity.get("presentacion")
            laboratorio = entity.get("laboratorio")
            directorTecnico = entity.get("directorTecnico")
            nombreComercial = entity.get("nombreComercial")
            #telefono = entity.get("telefono")
            #direccion = entity.get("direccion")
            #departamento = entity.get("departamento")
            #provincia = entity.get("provincia")
            #distrito = entity.get("distrito")
            #horarioAtencion = entity.get("horarioAtencion")
            ubigeo = entity.get("ubigeo")
            catCodigo = entity.get("catCodigo")
            email = entity.get("email")
            ruc = entity.get("ruc")
            
            
            if not precio1:
               precio1 = None
            else:    
               precio1 = f"{float(precio1):.2f}"
               
            if not precio2:
               precio2 = None
            else:    
               precio2 = f"{float(precio2):.2f}"  
               
            #if '--' in direccion:
             #   direccion = direccion.replace('--', ' ')
                
            #if '--' in telefono:
             #   telefono = telefono.replace('--', ' ')
                #
            product = ProductDigimid(
                #id_sku=ubigeo,
                ubigeo = ubigeo,
                nombre_producto=nombreProducto + " " + key_concent,
                concentracion=key_concent,
                presentacion=presentacion,
                precio1= precio1,                  
                precio2= precio2,
                pais_fabricacion=paisFabricacion,
                registro_sanitario=registroSanitario,
                condicion_venta=condicionVenta,
                tipo_producto=tipoProducto,
                nombre_titular=nombreTitular,
                nombre_fabricante=nombreFabricante,
                laboratorio=laboratorio,
                director_tecnico=directorTecnico,
                nombre_comercial=nombreComercial,
                #telefono=telefono,
                #direccion=direccion,
                #departamento=departamento,
                #provincia=provincia,
                #distrito=distrito,
                #horario_atencion=horarioAtencion,
                cat_codigo=catCodigo,
                email=email,
                ruc=ruc,
                cod_establecimiento = codEstablecimiento
                )
            return product
        except Exception as e: 
            print(f"{self.title} : Hubo error al parsear [entity] -> {str(e)}") 
            traceback.print_exc()     

        
        
            
        return None    

