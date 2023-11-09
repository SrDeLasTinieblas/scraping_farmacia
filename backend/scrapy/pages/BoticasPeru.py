import json
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page

    
class BoticasPeru(Page):
     
    def __init__(self, title = "Boticas Peru", url = "https://boticasperu.pe"):
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
        products_url = []
        conter = 0
        is_equals = True
        lastest_product_urls_hash = None
                
        while is_equals:
            conter += 1
            
            final_category_url =  f"{category_url}?p={conter}"
            print(f"Pag :: {final_category_url}")
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
              
                       
    def get_product(self, url_product):
        product = None
        
        html = download_page(url_product)
        if not html:
            print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
        
            title_text = soup.find('h1', class_='page-title').text.strip()
            
            sku_div = soup.find('div', class_='product attribute sku')
            strong_element = sku_div.find('div', class_='value')
            sku_text = strong_element.text.strip()
            
            product_info = {}  # Crear un diccionario para almacenar la información
            
            table = soup.find('tbody')
            
            if table:
                rows = table.find_all('tr')
                
                for row in rows:
                    header_cell = row.find('th', class_='col label')
                    data_cell = row.find('td', class_='col data')
                    
                    if header_cell and data_cell:
                        header_text = header_cell.text.strip()
                        data_text = data_cell.text.strip()
                        
                        product_info[header_text] = data_text
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
                first_item = list(target_json["data"]["items"].values())[0]
                nombre = first_item.get("images")
                name = nombre[0]["label"]

                prices_info = first_item.get("price_info")
                #final_price = prices_info["final_price"]
                regular_price = prices_info["regular_price"]
                
                
                product = Product(
                    id_sku = sku_text,
                    name =  name,
                    presentation =  None,
                    brand =  None,
                    price_box =  f"S/{regular_price:.2f}",
                    price_blister =  None,
                    source_information = self.title,
                    lifting_date =  None,
                    laboratory =  laboratorio,
                    card_discount =  None,
                    crossed_price =  None,
                    suggested_comment =  None
                )
                

            else:
                print("Elemento <script> no encontrado")    
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return product
    
    
    

    

    

    

