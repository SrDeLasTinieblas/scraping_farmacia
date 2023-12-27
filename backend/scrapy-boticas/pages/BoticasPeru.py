import json
import traceback
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page
import re
    
class BoticasPeru(Page):
     
    def __init__(self, id = 4, title = "Boticas Peru", url = "https://boticasperu.pe/"):
        super().__init__(id, title, url)
        self.name = title  # Agregar el atributo 'name'

    def get_categories(self):
        html = download_page(self.url)
               
        #categorys = []
        
        #categories_url = {}
        categories = []
        
        soup = BeautifulSoup(html, 'html.parser')
        if soup:
            nav_elements = soup.find_all('nav', class_='navigation')[0]
            li_elements = nav_elements.find_all('li', id=lambda x: x and x.startswith('vesitem-'))
            for li_element in li_elements:
                first_a_element = li_element.find('a')
                if first_a_element:
                    href_value = first_a_element.get('href')
                    title_value = first_a_element.find_all('span')[0].text
                    # print("title_value", title_value)
                    if href_value:
                        #categories[href_value] = title_value
                        #categories.append(Page(name=title_value, value=title_value))
                        categories.append({"id": href_value, "name": title_value})

                        #categorys.append(href_value)               
        print("categories: ", categories)
        return categories
    
    
    def get_product_urls(self, category_url):
        try:
            
            products_url = []
            conter = 0
            is_equals = True
            lastest_product_urls_hash = None
                    
            while is_equals:
                conter += 1
                
                final_category_url =  f"{category_url['id']}?p={conter}"
                #print(f"Pag :: {final_category_url}")
                products_url_internal = []
                
                try:
                    html = download_page(final_category_url)
                    if html:                                     
                        soup = BeautifulSoup(html, 'html.parser')
                        product_list = soup.find('ol', class_='products list items product-items')

                        if product_list:
                            product_items = product_list.find_all('li', class_='item product product-item')
                            
                            for item in product_items:
                                product_link = item.find('a')['href']
                                products_url_internal.append(product_link)
                                
                    else :
                        print(f"{self.title} : Hubo un error al descargar el category = {final_category_url}")  
                        products_url_internal = None           
                                
                except Exception as e:
                    
                    print(f"{self.title} : Hubo un error al extraer datos en {category_url} -> {str(e)}") 
                
                
                    
                if not products_url_internal:
                    continue
                            
                for product_url in products_url_internal:
                    products_url.append(product_url)                  

                
                my_tuple = tuple(products_url_internal) 
                hash_tuple = hash(my_tuple)
                
                if lastest_product_urls_hash == hash_tuple:
                    is_equals = False
                else:
                    lastest_product_urls_hash = hash_tuple         
            
            return products_url
        except Exception as e: 
            print(f"{self.title} : Hubo un error al extraer datos en -> {str(e)}")      

        return None
               
                 
    def get_MG(self, name):
        palabras_clave = ['ml', ' ml', ' gramos', 'gramos', 'mg', ' mg']#, 'un', ' un']
        
        #name = json["name"]
        
        if not name:
            mg_values = None
            
        mg_values = []
        for palabra in palabras_clave:
            #print("buscando valor: " + palabra)
            values = re.findall(rf'(\d+){palabra}', name.lower())
            mg_values.extend(values)
        
        if mg_values:
            primer_valor_mg_values = int(mg_values[0])
        elif not mg_values:
                primer_valor_mg_values = ''
                palabra = ''
            
        return primer_valor_mg_values, palabra
                     
                         
    def get_product(self, url_product):
        
        html = download_page(url_product)
        if not html:
            #print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None
        
        products = []
            
        try:
            
            soup = BeautifulSoup(html, 'html.parser')
        
            title_text = soup.find('h1', class_='page-title').text.strip()
            
            sku_div = soup.find('div', class_='product attribute sku')
            strong_element = sku_div.find('div', class_='value')
            sku_text = strong_element.text.strip()
            
            # Busca elementos con la clase "old-price"
            old_price_elements = soup.find_all(class_='price-box price-final_price')

            price_crossed = None  # Inicializar price_crossed antes del bucle

            # Busca elementos con la clase "old-price"
            old_price_elements = soup.find_all(class_='price-box price-final_price')

            # Itera a través de los elementos encontrados
            for element in old_price_elements:
                # Dentro de cada elemento "old-price", busca el precio con la clase "price"
                price_element = element.find(class_='old-price')
                # Si se encontró un precio, imprímelo y asigna el valor a price_crossed
                if price_element:
                    price_text = price_element.text.strip()
                    price_crossed = re.sub(r'[^\d.]', '', price_text)
                    #print("price_crossed: ", price_crossed)
                    
            product_info = {}  # Crear un diccionario para almacenar la información

            table = soup.find('tbody')
            # Inicializar laboratorio y price_crossed fuera del bucle
            laboratorio = None
            #price_crossed = None

            if table:
                rows = table.find_all('tr')

                # Inicializar laboratorio fuera del bucle
                laboratorio = None

                for row in rows:
                    header_cell = row.find('th', class_='col label')
                    data_cell = row.find('td', class_='col data')

                    if header_cell and data_cell:
                        header_text = header_cell.text.strip()
                        data_text = data_cell.text.strip()

                        product_info[header_text] = data_text

                        # Asignar valor a laboratorio solo si el encabezado es 'Laboratorio'
                        if header_text == 'Laboratorio':
                            laboratorio = data_text

            
            script_elements = soup.find_all('script', type='text/x-magento-init')
            target_json = None

            for script_element in script_elements:
                script_content = script_element.string
                data = json.loads(script_content)

                if "Magento_Catalog/js/product/view/provider" in script_content:
                    target_json = data["*"]["Magento_Catalog/js/product/view/provider"]
                    break
            
            
                
            if target_json:
                first_item = list(target_json["data"]["items"].values())[0]
                nombre = first_item.get("images")
                name = nombre[0]["label"]
                
                # Dividir la cadena desde la derecha usando " - " como delimitador
                parts = name.rsplit(" - ", 1)

                # Ahora, 'parts' es una lista con dos elementos, donde el último elemento es la presentación
                presentation = parts[-1]

                prices_info = first_item.get("price_info")
                final_price = prices_info["final_price"]
                
                primer_valor_mg_values, palabra = self.get_MG(name)

                product = Product(
                    id_sku = sku_text if name else None,
                    name =  name if name else None,
                    concentracion = str(primer_valor_mg_values) + str(palabra),
                    presentation =  presentation if presentation else None,
                    brand =  None,
                    price =  final_price if final_price else None,
                    source_information = self.title if self.title else None,
                    lifting_date =  None,
                    laboratory =  laboratorio if laboratorio else None,
                    card_discount =  None,
                    crossed_price =  price_crossed if price_crossed else None,
                    suggested_comment =  None,
                    description=None
                )
                products.append(product)
                

            else:
                print("Elemento <script> no encontrado")    
        except Exception as e:            
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
            traceback.print_exc()
            
        return products if products else None


    '''
    def get_product(self, url_product):
        html = download_page(url_product)
        
        if not html:
            print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None

        products = []

        try:
            soup = BeautifulSoup(html, 'html.parser')
            title_text = soup.find('h1', class_='page-title').text.strip()
            sku_div = soup.find('div', class_='product attribute sku')
            strong_element = sku_div.find('div', class_='value')
            sku_text = strong_element.text.strip()

            # Busca elementos con la clase "old-price"
            old_price_elements = soup.find_all(class_='price-box price-final_price')

            # Inicializar price_crossed antes del bucle
            price_crossed = None

            # Itera a través de los elementos encontrados
            for element in old_price_elements:
                # Dentro de cada elemento "old-price", busca el precio con la clase "price"
                price_element = element.find(class_='old-price')
                # Si se encontró un precio, imprímelo y asigna el valor a price_crossed
                if price_element:
                    price_text = price_element.text.strip()
                    price_crossed = re.sub(r'[^\d.]', '', price_text)
                    # print("price_crossed: ", price_crossed)

            product_info = {}  # Crear un diccionario para almacenar la información
            table = soup.find('tbody')

            # Inicializar laboratorio y price_crossed fuera del bucle
            laboratorio = None

            if table:
                rows = table.find_all('tr')

                for row in rows:
                    header_cell = row.find('th', class_='col label')
                    data_cell = row.find('td', class_='col data')

                    if header_cell and data_cell:
                        header_text = header_cell.text.strip()
                        data_text = data_cell.text.strip()

                        product_info[header_text] = data_text

                        # Asignar valor a laboratorio solo si el encabezado es 'Laboratorio'
                        if header_text == 'Laboratorio':
                            laboratorio = data_text

            script_elements = soup.find_all('script', type='text/x-magento-init')
            target_json = None

            for script_element in script_elements:
                script_content = script_element.string
                data = json.loads(script_content)

                if "Magento_Catalog/js/product/view/provider" in script_content:
                    target_json = data["*"]["Magento_Catalog/js/product/view/provider"]
                    break

            if target_json:
                first_item = list(target_json["data"]["items"].values())[0]
                nombre = first_item.get("images")
                name = nombre[0]["label"]

                # Dividir la cadena desde la derecha usando " - " como delimitador
                parts = name.rsplit(" - ", 1)

                # Ahora, 'parts' es una lista con dos elementos, donde el último elemento es la presentación
                presentation = parts[-1]

                prices_info = first_item.get("price_info")
                final_price = prices_info["final_price"]

                product = Product(
                    id_sku=sku_text if name else None,
                    name=name if name else None,
                    presentation=presentation if presentation else None,
                    brand=None,
                    price=final_price if final_price else None,
                    source_information=self.title if self.title else None,
                    lifting_date=None,
                    laboratory=laboratorio if laboratorio else None,
                    card_discount=None,
                    crossed_price=price_crossed if price_crossed else None,
                    suggested_comment=None,
                    description=None
                )
                products.append(product)

            else:
                print("Elemento <script> no encontrado")

        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")
            traceback.print_exc()

        return products if products else None
    '''

    

    
