from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page

class BoticasHogarSalud(Page):
    
    def __init__(self, title = "Hogar y Salud", url = "https://www.hogarysalud.com.pe"):
        super().__init__(title, url)

    
    def get_categories(self):   
        html = download_page(self.url)
        category_urls = []
        
        soup = BeautifulSoup(html, 'html.parser')
        elements_menu_item = soup.find_all('li', id=lambda x: x and x.startswith('menu-item-'))

        for element in elements_menu_item:
            href = element.find('a')["href"] 
            if href and href.startswith(f"{self.url}/c/"):
                category_urls.append(href)

        all_products_urls = []  # Almacena todos los enlaces de productos de todas las categorías
        
        #category_urls = category_urls[:1]  # Limitar a una categoría (para pruebas)
        for category_url in category_urls:
            product_urls_in_category = self.get_all_products_in_category(category_url)
            all_products_urls.extend(product_urls_in_category)

        print("Total de enlaces de productos de todas las categorías:", len(all_products_urls))
        return list(set(category_urls))
    
    def get_all_products_in_category(self, category_url):
        products_url = []
        conter = 0  # Inicializa el contador en 0
        is_equals = True
        lastest_product_urls_hash = None
        no_pagination_url_tried = False
                    
        while is_equals:
            conter += 1  # Aumenta el contador en cada iteración
            final_category_url = category_url
                    # https://www.hogarysalud.com.pe/c/salud-y-bienestar/?per_page=100
                    # https://www.hogarysalud.com.pe/c/salud-y-bienestar/page/2/?per_page=100
                    
            if conter == 1:
                final_category_url = f"{category_url}?per_page=36"
            elif conter >= 2:
                final_category_url = f"{category_url}page/{conter}/?per_page=36"
                
            print(f"Pag :: {final_category_url}")
            html = download_page(final_category_url)
            
            if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    product_list = soup.find('ol', class_='products list items product-items')

                    if product_list:
                        product_items = product_list.find_all('li', class_='item product product-item')
                            
                        for item in product_items:
                            product_link = item.find('a')['href']
                            products_url_internal.append(product_link)
                            
            else:
                if conter == 1:
                    no_pagination_url_tried = True
                else:
                    break  # Sale del bucle si no hay más productos en la página

            '''
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
                            
                else:
                    if conter == 1:
                        no_pagination_url_tried = True
                    else:
                        break  # Sale del bucle si no hay más productos en la página

            except Exception as e:
                print(f"{self.title} : Hubo un error al extraer datos en {final_category_url} -> {str(e)}")

            if not products_url_internal:
                continue

            for product_url in products_url_internal:
                products_url.append(product_url)
                
            if no_pagination_url_tried and conter == 1:
                break  # Sale del bucle si se intentó sin numeración y no se obtuvieron productos
            conter += 1  # Aumenta el contador solo si no se produjo un error
            '''
        
        return products_url


                    
                            
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
            sku_id = soup.find('input', {'name': 'gtm4wp_sku'})["value"]
            select_element = soup.find('select', {'id': 'pa_venta-por'})
            price_element = soup.find('p', class_='price')
            price_spans = price_element.find_all('span', class_='woocommerce-Price-amount amount')

            precios = []
            presentaciones = None 
            
            for span in price_spans:
                precio_text = span.bdi.get_text(strip=True)
                precio_text = precio_text.replace('S/', '').strip()
                
                precio_float = float(precio_text)
                precios.append(precio_float)

            
            if select_element:
                opciones = select_element.find_all('option')
                
                presentacion = [opcion.text.strip() for opcion in opciones if opcion.get('value')]
                
                presentaciones = " / ".join(presentacion)
                
            product = Product(
                id_sku=sku_id if sku_id else None,
                name=name if name else None,
                presentation=presentaciones if presentaciones else None,
                brand=None, 
                price_box=f"S/{precios[1]:.2f}" if precios and len(precios) > 1 else None,
                price_blister=f"S/{precios[0]:.2f}" if precios and len(precios) > 0 else None,
                source_information=self.title if self.title else None,
                lifting_date=None,  
                laboratory=None,  
                card_discount=None,  
                crossed_price=f"S/{price_box:.2f}" if price_box else None,
                suggested_comment=None 
            )

            
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return product