import requests
import json
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_json, download_page, get_random_user_agent

class BoticasSalud(Page):
    
    def __init__(self, title = "Boticas y Salud", url = "https://www.boticasysalud.com"):
        super().__init__(title, url)

    def get_categories(self):
        url = "https://bys-prod-backend.azurewebsites.net/api/ServiceCategory"
        response_data = download_json(url)
        data = response_data["data"]
        category_slugs = []
        for category in data:
            slug = category["slug"]
            
            category_slugs.append(slug)
        return category_slugs
    
    def get_product_urls(self, category_slug):
        url = f"https://bys-prod-backend.azurewebsites.net/api/ServiceProduct?filterValue={category_slug}&filterBy=2&CurrentPage=1&PageSize=1"
        response_data = download_json(url)
        if not response_data:
            print(f"{self.title} : Hubo un error al descargar category = {category_slug}")
            return None
        
        total_items = response_data["data"]["totalItems"]
        url = f"https://bys-prod-backend.azurewebsites.net/api/ServiceProduct?filterValue={category_slug}&filterBy=2&CurrentPage=1&PageSize={total_items}"
        response_data = download_json(url)
        
        products_slug = []

        data = response_data["data"]["data"]
        for item in data:
            slug = item["slug"]
            if slug:
                products_slug.append(slug)             
            
        return products_slug    
              
                       
    def get_product(self, product_slug):
        product = None
        
        url = f"https://bys-prod-backend.azurewebsites.net/api/ServiceProduct/getbyparameters?FilterValue={product_slug}&FilterBy=2"
        response_data = download_json(url)
        #url_web = f"https://www.boticasysalud.com/tienda/productos/{product_slug}"
        #response_data_web = download_page(url_web)
        
        if not response_data:
            print(f"{self.title} : Hubo un error al descargar el producto = {product_slug}")
            return None
        
        try:
            
            titulos = []
            
            item = response_data["data"]
            categoria = item["categories"][0]
            titulo_categoria = categoria["title"]
            
            title = item["title"]
            
            #discounted_price = item["discountedPrice"]
            #presentations = item["presentations"][0]
            presentations = item["presentations"]
            discounted_price = response_data["data"]["presentations"][0]["discountedPrice"]
            #titulos = presentations["title"]
            #print(discounted_price)
            
            for presentation in presentations:
                titulo = presentation["title"]  # Obtiene el título de la presentación actual
                titulos.append(titulo)  # Agrega el título a la lista de títulos

            # Ahora, la lista "titulos" contendrá todos los títulos de las presentaciones
            #print(titulos)
            presentation_titles = " / ".join(titulos)
            # Inicializa un array para almacenar los precios
            precios = []

            # Inicializa listas para almacenar las presentaciones y precios
            presentation_titles = []
            prices_blister = []
            prices_box = []

            # Itera a través de las presentaciones y extrae los precios
            for presentation in item["presentations"]:
                title_presentacion = presentation["title"]
                precio = presentation["price"]
                presentation_title = f"{title_presentacion} x {presentation['fractions']} {presentation['description']}"
                presentation_titles.append(presentation_title)
                precios.append(precio)

                if title_presentacion == "Blister":
                    prices_blister.append(precio)
                elif title_presentacion == "Caja":
                    prices_box.append(precio)
                else:
                    # Si no es "Blister" ni "Caja," asumir que es una caja
                    prices_box.append(precio)

            #print("precio: ", precio)

            product_brand = item["productBrand"]
            brand = product_brand["title"]
            sku_id = item["skuIdClient"]

            laboratorio = next((details["description"] for details in item["details"] if details["name"] == "Laboratorio"), None)

            crossed_price = 0
            if discounted_price > 0:
                 crossed_price = prices_box[0]
                 
            product = Product(
                id_sku=sku_id if sku_id else None,
                name=title if title else None,
                presentation=" / ".join(presentation_titles) if presentation_titles else None,
                brand=brand,
                price_box=f"{prices_box[0]:.2f}" if prices_box else None,
                price_blister=f"{prices_blister[0]:.2f}" if prices_blister else None,
                source_information=self.title if self.title else None,
                lifting_date=None,
                laboratory=laboratorio if laboratorio else None,
                card_discount=f"{discounted_price:.2f}" if discounted_price else None,
                crossed_price=crossed_price,
                suggested_comment=None
            )



        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {product_slug} -> {str(e)}")          
            
            
        return product
    
    
    

    

    

    


