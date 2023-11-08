from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page

class BoticasHogarSalud(Page):
    
    def __init__(self, title = "Hogar y Salud", url = "https://www.hogarysalud.com.pe"):
        super().__init__(title, url)

    def get_categories(self):   
        html = download_page(self.url)
               
        categorys = []        
        soup = BeautifulSoup(html, 'html.parser')
        elements_menu_item = soup.find_all('li', id=lambda x: x and x.startswith('menu-item-'))

        for element in elements_menu_item:
            href = element.find('a')["href"] 
            if href:
                if href.startswith(f"{self.url}/c/"):
                    categorys.append(href)       
                             
        return list(set(categorys))
    
    
    def get_product_urls(self, category_url):
        html = download_page(category_url)
        if not html:
            print(f"{self.title} : Hubo un error al descargar el category = {category_url}")
            return None

        product_urls = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            matching_links = soup.find_all('a', class_='product-image-link')
            for link in matching_links:
                href = link.get('href')
                product_urls.append(href)

           
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {category_url} -> {str(e)}") 
                            
        return product_urls    
                    
                            
    def get_product(self, url_product):
        product = None
                
        html = download_page(url_product)
        if not html:
            print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None         
    
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            name = soup.find('input', {'name': 'gtm4wp_name'})["value"]
            price_box = soup.find('input', {'name': 'gtm4wp_price'})["value"]               
            price_box = float(price_box)
            crossed_price = ""
            
            product = Product(
                    name =  name,
                    presentation =  None,
                    brand =  None,
                    price_box =  f"S/{price_box:.2f}",
                    price_blister =  f"S/{price_box:.2f}",
                    source_information = self.title,
                    lifting_date =  None,
                    laboratory =  None,
                    card_discount =  None,
                    crossed_price =  f"S/{price_box:.2f}",
                    suggested_comment =  None
                )
            
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return product