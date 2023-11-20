import json
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_json, download_page
from utils.Utils import unique_text, decode_base64, hyphenated_string_to_tuple, tuple_to_hyphenated_string

class Digemid(Page):
    
    def __init__(self, id = 6, title = "Digemid", url = "https://opm-digemid.minsa.gob.pe"):
        super().__init__(id, title, url)
    
    
    def get_categories(self):           
        categories = {}
        url = decode_base64("aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL1NyRGVMYXNUaW5pZWJsYXMvTWluc2FfZGF0YS9tYWluL21pbnNhX3BoYXJtYWNldXRpY2FsX3Byb2R1Y3RzLmpzb24=")
        categories[url] = "main"        
        return categories
    
    def get_product_urls(self, category_url):
        response_json = download_json(category_url)
        
        # 1) Del Json obtener los nombres del producto "Nom_Prod" -> Ejemplo = DAVINTEX 120
        
        first_five_words_list = []
        for item in response_json:
            # Example : 3A OFTENO
            # Example : BENZOATO DE BENCILO 
            name_product = item["Nom_Prod"]
            first_five_words = name_product[:5] 
            first_five_words_list.append(first_five_words)
        
        first_five_words_list = list(set(first_five_words_list))  
       
        
        request_data_dic = {}
        
        
        for first_five_words in first_five_words_list[:10]:
            search_word = first_five_words  
                      
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
                continue
            
            data = response_json["data"]
            if not data:
                continue
            
            for item in data:                
                grupo = item["grupo"]
                concent = item["concent"]
                codGrupoFF = item["codGrupoFF"]  
                             
                """
                    El id se forma asi grupo|concent|codGrupoFF
                    Ejemplo =           2926|120mg/5mL\t|24
                    
                """                        
                original_tuple = (grupo, concent, codGrupoFF)
                build_id = tuple_to_hyphenated_string(original_tuple)
                request_data_dic[build_id] = original_tuple
         
        product_ids = [] 
        for key, truple_data in request_data_dic.items():            
            product_ids.append(key)                 
                                    
        return product_ids           
         
                            
    def get_product(self, product_id):   
        # El product_id que llega es  2926|120mg/5mL\t|24 
        item_tuple = hyphenated_string_to_tuple(product_id)
        product_code = item_tuple[0]
        concent = item_tuple[1]
        codGrupoFF = item_tuple[2]
        
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
            "nombreProducto": None
        }
        })
        headers = {
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
            print(f"{self.title} : Hubo un error al descargar el producto = {product_id}")
            return None         
        
        data = response_json["data"]
        if not data:
            print(f"{self.title} : Hubo un error al obtener [data] en el producto = {product_id}")
            return None
        
        products_dic = {}   
        products = []
        
        try:
            for item in data:
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
                
                #if "S/" in precio:
                 #   try:
                  #      precio = float(precio.replace('S/', ''))
                   # except ValueError:
                    #    precio = 0.0  # O asigna cualquier otro valor predeterminado que desees


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
                    presentation =  None,
                    brand = None,
                    price =  f"{float(precio):.2f}",
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
            print(f"{self.title} : Hubo un error al extraer datos en {product_id} -> {str(e)}")      

        for key, product in products_dic.items():            
                products.append(product)        
    
    
    
        return products if products else None
    
    
    def get_product_more_details(self, product):
        """
            For next call need data
            codigoProducto":53725,"         ====> codProdE  ====> name
            codEstablecimiento":"0053974"   ====> codEstab  ====> id_sku
        """
        codigoProducto = int(product.name)
        codEstablecimiento = f"{product.id_sku}" 
        
        url_post = "https://ms-opm.minsa.gob.pe/msopmcovid/precioproducto/obtener"

        payload = json.dumps({
        "filtro": {
            "codigoProducto": codigoProducto,
            "codEstablecimiento": codEstablecimiento,
            "tokenGoogle": ""
        }
        })
        headers = {
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

        if response_json is not None:
            #print("response: ", response_json) ------

            entity = response_json.get("entidad")
            if entity is not None:
                #print("Entidad: ", entity) -----
                price = entity.get("precio1")
                name = entity.get("nombreProducto")
                laboratory = entity.get("laboratorio")
                presentation = entity.get("presentacion")
                farma = entity.get("nombreComercial")
                ubigeo = entity.get("ubigeo")

                #if "S/" in price:
                  #  try:
                   #     price = float(price.replace('S/', ''))
                    #except ValueError:
                     #   price = 0.0  # O asigna cualquier otro valor predeterminado que desees

                product = Product(
                        id_sku=ubigeo,
                        name=name,
                        presentation=presentation,
                        brand=None,
                        price=f"{float(price):.2f}",
                        source_information=f"{self.title}",#-{farma}
                        lifting_date=None,
                        laboratory=laboratory,
                        card_discount=None,
                        crossed_price=None,
                        suggested_comment=None,
                        description=None
                    )
                return product

        return None