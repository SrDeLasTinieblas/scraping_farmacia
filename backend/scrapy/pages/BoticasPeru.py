import json
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page

    
class BoticasPeru(Page):
    
    def __init__(self, title, url):
        super().__init__(title, url)

    def get_categories(self):
        html = download_page(self.url)
               
        categorys = []
        
        soup = BeautifulSoup(html, 'html.parser')
        nav_elements = soup.find_all('nav', class_='navigation')[0]
        li_elements = nav_elements.find_all('li', id=lambda x: x and x.startswith('vesitem-'))
        for li_element in li_elements:
            first_a_element = li_element.find('a')
            if first_a_element:
                href_value = first_a_element.get('href')
                if href_value:
                    categorys.append(href_value)               
        
        return categorys
    
    
    def get_product_urls(self, category_url):
        html = download_page(category_url)
        if not html:
            print(f"Hubo un error al descargar el category = {category_url}")
            return None

        product_urls = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            product_list = soup.find('ol', class_='products list items product-items')

            if product_list:
                product_items = product_list.find_all('li', class_='item product product-item')

                for item in product_items:
                    product_link = item.find('a')['href']
                    product_urls.append(product_link)
        except Exception as e:
            print(f"Hubo un error al extraer datos en {category_url} -> {str(e)}") 
                            
        return product_urls    
              
                       
    def get_product(self, url_product):
        product = None
        
        html = download_page(url_product)
        if not html:
            print(f"Hubo un error al descargar el producto = {url_product}")
            return None
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
        
            title_text = soup.find('h1', class_='page-title').text.strip()
            
            product_info = {}  # Crear un diccionario para almacenar la información
            
            # Buscar la tabla dentro de <tbody>
            table = soup.find('tbody')
            
            if table:
                # Buscar todas las filas <tr> dentro de la tabla
                rows = table.find_all('tr')
                
                for row in rows:
                    # Encontrar las celdas <th> y <td> dentro de cada fila
                    header_cell = row.find('th', class_='col label')
                    data_cell = row.find('td', class_='col data')
                    
                    if header_cell and data_cell:
                        # Obtener el texto dentro de las celdas y eliminar espacios en blanco
                        header_text = header_cell.text.strip()
                        data_text = data_cell.text.strip()
                        
                        # Almacenar la información en el diccionario
                        product_info[header_text] = data_text
                        # Imprimir el diccionario con la información
                        laboratorio = product_info.get('Laboratorio', None)

            
            script_elements = soup.find_all('script', type='text/x-magento-init')
            target_json = None

            for script_element in script_elements:
                script_content = script_element.string
                data = json.loads(script_content)

                if "Magento_Catalog/js/product/view/provider" in script_content:
                    target_json = data["*"]["Magento_Catalog/js/product/view/provider"]
                    break

            if target_json:
                # print("\mtarget_json ->", target_json)
                # print("\n\n")
                first_item = list(target_json["data"]["items"].values())[0]
                nombre = first_item.get("images")
                nombre_label = nombre[0]["label"]

                prices_info = first_item.get("price_info")
                final_price = prices_info["final_price"]
                regular_price = prices_info["regular_price"]
                
                product = Product(
                    name =  nombre_label,
                    presentation =  None,
                    brand =  None,
                    price_box =  f"S/{final_price:.2f}",
                    price_blister =  f"S/{regular_price:.2f}",
                    source_information =  None,
                    lifting_date =  None,
                    laboratory =  laboratorio,
                    card_discount =  None,
                    crossed_price =  f"S/{regular_price:.2f}",
                    suggested_comment =  None
                )
                

            else:
                print("Elemento <script> no encontrado")    
        except Exception as e:
            print(f"Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return product
    
    
    

    

    

    

