import json
import re
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page

class HogarSalud(Page):
    
    def __init__(self, id = 5, title = "Hogar y Salud", url = "https://www.hogarysalud.com.pe"):
        super().__init__(id, title, url)
        self.name = title  # Agregar el atributo 'name'

    
    def get_categories(self):   
        try:
            html = download_page(self.url)
            soup = BeautifulSoup(html, 'html.parser')
            
            categories = []
            category = {}
            elements_menu_item = soup.find_all('li', id=lambda x: x and x.startswith('menu-item-'))

            for element in elements_menu_item:
                a_element = element.find("a")
                if a_element:
                    href = a_element.get("href", "")
                    if href.startswith(f"{self.url}/c/"):
                        title_element = a_element.find('span', class_='nav-link-text')
                        #print("title_element: ", title_element)
                        if title_element:
                            title = title_element.text
                            category[href] = title
                            categories.append({"id": href, "name": title })

            return categories

        except Exception as e:
            print(f"Error: {e}")
            return None

    
    def get_categories2(self):
        html = download_page(self.url)
        
        categories = {}
        
        soup = BeautifulSoup(html, 'html.parser')
        elements_menu_item = soup.find_all('li', id=lambda x: x and x.startswith('menu-item-'))

        for element in elements_menu_item:
            a_element = element.find("a")
            if a_element:
                href = a_element["href"] 
                if href and href.startswith(f"{self.url}/c/"):
                    title_element = a_element.find('span', class_='nav-link-text')
                    if title_element:
                        title = title_element.text
                        categories[href] = title
                    
        """
        html = download_page(self.url)
        
        categories = {}
        
        soup = BeautifulSoup(html, 'html.parser')
        elements_menu_item = soup.find_all('li', id=lambda x: x and x.startswith('menu-item-'))

        for element in elements_menu_item:
            a_element = element.find("a")
            href = a_element["href"] 
            print("a_element: ", a_element)
            if href and href.startswith(f"{self.url}/c/"):
                #category_urls.append(href)
                print("href", href)
                title = a_element.find('span', class_='nav-link-text')
                if title:
                    title = title.text
                    categories[href] = title
        """

        """  
        
        all_products_urls = []  # Almacena todos los enlaces de productos de todas las categorías
        
        #category_urls = category_urls[:1]  # Limitar a una categoría (para pruebas)
        for category_url in category_urls:
            product_urls_in_category = self.get_all_products_in_category(category_url)
            all_products_urls.extend(product_urls_in_category)

        print("Total de enlaces de productos de todas las categorías:", len(all_products_urls))
        
        """ 
        
        
        
        return categories
    
    
    def get_product_urls(self, category_url):
        products_url = []
        conter = 0  # Inicializa el contador en 0
        is_not_error = True
        try:
                        
            while is_not_error:
                conter += 1  # Aumenta el contador en cada iteración
                final_category_url = category_url["id"]
                        # https://www.hogarysalud.com.pe/c/salud-y-bienestar/?per_page=100
                        # https://www.hogarysalud.com.pe/c/salud-y-bienestar/page/2/?per_page=100
                        
                if conter == 1:
                    final_category_url = f"{category_url['id']}?per_page=36"
                elif conter >= 2:
                    final_category_url = f"{category_url['id']}page/{conter}/?per_page=36"
                    
                #print(f"Pag :: {final_category_url}")
                html = download_page(final_category_url)
                
                if html:
                        soup = BeautifulSoup(html, 'html.parser')
                        matching_links = soup.find_all('a', class_='product-image-link')
                        for link in matching_links:
                            href = link.get('href')
                            products_url.append(href)
                                    
                else:
                    if conter == 1:
                        no_pagination_url_tried = True
                    else:
                        # is_not_error = True
                        break  # Sale del bucle si no hay más productos en la página

            return products_url             
        except Exception as e: 
            print(f"{self.title} : Hubo un error al extraer datos en {category_url['id']} -> {str(e)}")      

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
            print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None         
    
        products = []
        try:

            soup = BeautifulSoup(html, 'html.parser')
            
            
            name = soup.find('input', {'name': 'gtm4wp_name'})["value"]
            sku_id = soup.find('input', {'name': 'gtm4wp_sku'})["value"]

            
            forms = soup.find_all('form')
            primer_valor_mg_values, palabra = self.get_MG(name)

            is_single = True
            for form in forms:
                if form.has_attr('data-product_variations'):
                 
                    presentaciones = json.loads(form["data-product_variations"]) 
                    for presentacion in presentaciones:
                        price = presentacion["display_regular_price"]
                        description_presentacion = presentacion["variation_description"]
                        presentacion_attr = presentacion["attributes"]["attribute_pa_venta-por"]
                        
                        product = Product(
                            id_sku=sku_id if sku_id else None,
                            name=name if name else None,
                            concentracion = str(primer_valor_mg_values) + str(palabra),
                            presentation = presentacion_attr if presentacion_attr else None,
                            brand=None, 
                            price=f"{price:.2f}" if price else None,
                            source_information=self.title if self.title else None,
                            lifting_date=None,  
                            laboratory=None,  
                            card_discount=None,  
                            crossed_price=None,
                            suggested_comment=None,
                            description= description_presentacion if description_presentacion else None 
                        )
                        products.append(product)
                                              
                    is_single = False
                    break
                        
                        
            
            if is_single:
                            
                price = soup.find('input', {'name': 'gtm4wp_price'})["value"]               
                price = float(price) 
                
                crossed_price = None  
                                
                price_element = soup.select_one('p.price')
                prices_str = [span.get_text(strip=True) for span in price_element.find_all('span', class_='woocommerce-Price-amount')]
                prices_float = [float(precio.replace('S/', '')) for precio in prices_str]

                if len(prices_float) == 2:
                    crossed_price = max(prices_float)
                    price = min(prices_float)
                                                                                               
                            
                product = Product(
                    id_sku=sku_id if sku_id else None,
                    name=name if name else None,
                    presentation = None,
                    brand=None, 
                    price=f"{price:.2f}" if price else None,
                    source_information=self.title if self.title else None,
                    lifting_date=None,  
                    laboratory=None,  
                    card_discount=None,  
                    crossed_price=f"{crossed_price:.2f}" if crossed_price else None,
                    suggested_comment=None,
                    description=None 
                )
                products.append(product)
            
            
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return products if products else None