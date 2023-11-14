from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_json, download_page
import re

class BoticasFarmaUniversal(Page):
    
    def __init__(self, title = "Boticas Farma Universal", url = "https://farmaciauniversal.com/"):
        super().__init__(title, url)

    def get_categories(self):
        html = download_page(self.url)
        soup = BeautifulSoup(html, 'html.parser')
                
        categorys = [] 
        nav_element = soup.find('nav', {'id': 'cabecera-productos'})
        products_link = nav_element.find_all('a', href=lambda href: href and href.startswith('productos'))
        for link in products_link:
            href = link["href"]
            # href default  ==  productos/18-ortopedia
            # https://farmaciauniversal.com/productos/18-ortopedia
            if href.startswith('productos'):
                href = f"{self.url}/{href}"
            categorys.append(href)

        return categorys
    
    
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
            
            print("payload", payload)
            #print("categoria::.", post_url)
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
        product = None        
        html = download_page(url_product)
        if not html:
            print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None
            
        try:
            soup = BeautifulSoup(html, 'html.parser')     
            name = soup.find('meta', {'property': 'og:title'})["content"]

            productos_datos = soup.find('div', {'id': 'productos_datos'})
            #print("productos_datos", productos_datos)
            
            price = productos_datos.find('div', {'class': 'float'}).find('strong')
            price = price.text
           
            crossed_price = productos_datos.find('div', {'class': 'float pregular2'}).find('span')
            if crossed_price:
               crossed_price = crossed_price.text
                
            product = Product(
                    #id_sku =  if sku_id else None
                    name =  name if name else None,
                    presentation =  None,
                    brand =  None,
                    price_box =  price if price else None,
                    price_blister =  price if price else None,
                    source_information = self.title if self.title else None,
                    lifting_date =  None,
                    laboratory =  None,
                    card_discount =  None,
                    crossed_price =  crossed_price if crossed_price else None,
                    suggested_comment =  None
            )  
                    
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return product