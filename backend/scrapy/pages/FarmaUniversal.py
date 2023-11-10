import traceback
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_json, download_page
import re

class FarmaUniversal(Page):
    
    def __init__(self, id = 1, title = "Farma Universal", url = "https://farmaciauniversal.com"):
        super().__init__(id, title, url)

    def get_categories(self):
        html = download_page(self.url)
        soup = BeautifulSoup(html, 'html.parser')
                
        categories = {} 
        nav_element = soup.find('nav', {'id': 'cabecera-productos'})
        products_link = nav_element.find_all('a', href=lambda href: href and href.startswith('productos'))
        for link in products_link:
            href = link["href"]
            # href default  ==  productos/18-ortopedia
            # https://farmaciauniversal.com/productos/18-ortopedia
            if href.startswith('productos'):
                title = link.find("b").text
                href = f"{self.url}/{href}"
                categories[href] = title

        return categories
    
    
    def get_product_urls(self, category_url):
        category_id = None
        product_urls = []
                   
        match = re.search(r'/productos/(\d+)-', category_url)
        
        if match:
            category_id = match.group(1)            
        else:
            print(f"{self.title} : Hubo un error, category id no encontrado = {category_url}")
            return None
        
        """
        payload is  orden=  &   idcate=4    &   idsubcate=0     &offset=32  &scroll=true
        response is offset = 48     tot_result = 16        
    
        """
        there_are_more_pages = True   
        last_total_result = 0    
       
        while there_are_more_pages:       
            post_url = f"{self.url}/productos/cargarproductos"
            offset = last_total_result
            payload = f"orden=&idcate={category_id}&idsubcate=0&offset={offset}&scroll=true"
            
            #print("payload", payload)
            print("categoria::.", post_url)
            headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': f"{self.url}",
            'Connection': 'keep-alive',
            'Referer': f"{category_url}",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            }
                    
            response_data = download_json(url = post_url, method="POST", headers=headers, data=payload)
            
            html_data = response_data["html"]                
            response_last_total_result = response_data["tot_result"]  
                          
            if response_last_total_result:
                last_total_result += response_last_total_result              
                          
            if response_last_total_result == 0:
                there_are_more_pages = False
                continue   
            
             
            
            # offset = response_data["offset"]
            soup = BeautifulSoup(html_data, 'html.parser')
            products_elements = soup.find_all('a', href=lambda href: href and href.startswith('producto'))
            for link in products_elements:
                href = link["href"]
                # href default  ==  producto\/detalle\/416-headshoulders-hidratacion-coco-shampoo-x-180-ml\
                # https://farmaciauniversal.com/producto/detalle/30/304/pantene-rizos-definidos-acondicionador-x-400-ml
                if href.startswith('producto'):
                    href = f"{self.url}/{href}"
                
                product_urls.append(href)   
                 
        return product_urls    
                    
                            
    def get_product(self, url_product):
        html = download_page(url_product)
        if not html:
            print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None
            
        products = []    
            
        try:
            soup = BeautifulSoup(html, 'html.parser')     
            name = soup.find('meta', {'property': 'og:title'})["content"]

            productos_datos = soup.find('div', {'id': 'productos_datos'})
            #print("productos_datos", productos_datos)
            
            price = productos_datos.find('div', {'class': 'float'}).find('strong')
            price = price.text
           
            crossed_price = productos_datos.find('div', {'class': 'float pregular2'})
            if crossed_price:
               crossed_price = crossed_price.find('span')
               if crossed_price:
                  crossed_price = crossed_price.text
                
            product = Product(
                    id_sku = None,
                    name =  name if name else None,
                    presentation =  None,
                    brand =  None,
                    price =  price if price else None,
                    source_information = self.title if self.title else None,
                    lifting_date =  None,
                    laboratory =  None,
                    card_discount =  None,
                    crossed_price =  crossed_price if crossed_price else None,
                    suggested_comment =  None,
                    description=None
            )  
            products.append(product)
                    
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
            traceback.print_exc()

    
        return products if products else None