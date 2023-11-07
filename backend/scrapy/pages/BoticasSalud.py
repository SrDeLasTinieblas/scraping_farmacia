import requests
import json
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page, get_random_user_agent
import requests
from bs4 import BeautifulSoup
import json
class BoticasSalud(Page):
    def __init__(self, title, url):
        super().__init__(title, url)

    def get_categories(self):
        url = "https://bys-prod-backend.azurewebsites.net/api/ServiceCategory"

        user_agent = get_random_user_agent()
        my_headers = {
            "User-Agent": user_agent
        }

        payload = {}

        response = requests.get(url, headers=my_headers, data=payload)
        response_data = json.loads(response.text)

        data = response_data["data"]

        category_slugs = []

        # Itera sobre cada categoría
        for category in data:
            slug = category["slug"]
            url_base = f"https://www.boticasysalud.com/tienda/catalogo/{slug}"
            category_slugs.append(url_base)
        return category_slugs

    def get_all_products_in_category(self, categoria_url):
        # Obtener el total de elementos en la categoría
        total_items = self.get_total_items_in_category(categoria_url)

        # Hacer una solicitud para obtener todos los productos de la categoría
        products = self.get_products_in_category(categoria_url, total_items)
        print(products)

        return products

    def get_total_items_in_category(self, categoria_url):
        url = f"https://bys-prod-backend.azurewebsites.net/api/ServiceProduct?filterValue={categoria_url}&filterBy=2&CurrentPage=1&PageSize=1"

        user_agent = get_random_user_agent()
        my_headers = {
            "User-Agent": user_agent
        }

        payload = {}

        response = requests.get(url, headers=my_headers, data=payload)
        response_data = json.loads(response.text)

        total_items = response_data["data"]["totalItems"]
        return total_items
    
    def get_laboratory(self, slug):
        try:

            url = f"https://bys-prod-backend.azurewebsites.net/api/ServiceProduct/getbyparameters?FilterValue={slug}&FilterBy=2"
            response = requests.get(url)

            # Asegúrate de que la solicitud haya sido exitosa antes de continuar
            if response.status_code == 200:
                response_data = response.json()
                
                # Accede a los datos dentro del objeto Python
                data = response_data["data"]

                # Ahora puedes acceder a los detalles
                details = data.get("details", [])
                
                for detail in details:
                    name = detail.get("name", "")
                    description = detail.get("description", "")
                    order = detail.get("order", "")

                    #print("Nombre:", name)
                    #print("Descripción:", description)
                    #print("Orden:", order)
                    if(name == "Laboratorio"):
                        return description

        except Exception as e:
            print(f"Error al obtener el laboratorio: {str(e)}")
            return {str(e)}


    def get_products_in_category(self, categoria_url, total_items):
        url = f"https://bys-prod-backend.azurewebsites.net/api/ServiceProduct?filterValue={categoria_url}&filterBy=2&CurrentPage=1&PageSize={total_items}"

        user_agent = get_random_user_agent()
        my_headers = {
            "User-Agent": user_agent
        }

        payload = {}

        response = requests.get(url, headers=my_headers, data=payload)
        response_data = json.loads(response.text)

        data = response_data["data"]["data"]

        products = []
        slug_productos = []
        urls_productos = []
        slug = ""
        laboratorio = ""
        total_items = response_data["data"]["totalItems"]

        print("total_items: ", total_items)

        for item in data:
            nombre = item["title"]
            discounted_price = item["discountedPrice"]
            dispresentation = item["presentation"]
            slug = item["slug"]
            title_presentation = dispresentation["title"]
            description = dispresentation["description"]
            normal_price = dispresentation["price"]
            presentation = title_presentation + description

            product_brand = item["productBrand"]
            brand = product_brand["title"]

            slug_productos.append(slug)

            laboratorio = self.get_laboratory(f"{slug}")
        
        product = Product(
            name=nombre,
            presentation=title_presentation,
            brand=brand,
            price_box=None,
            price_blister=f"S/{normal_price:.2f}",
            source_information=None,
            lifting_date=None,
            laboratory=laboratorio,
            card_discount=f"S/{discounted_price:.2f}",
            crossed_price=None,
            suggested_comment=None
            )

        products.append(product)

        return products



'''
    def get_products_in_category(self, categoria_url):
        total_items = 12
        url = f"https://bys-prod-backend.azurewebsites.net/api/ServiceProduct?filterValue={categoria_url}&filterBy=2&CurrentPage=1&PageSize={total_items}"

        user_agent = get_random_user_agent()
        my_headers = {
            "User-Agent": user_agent
        }

        payload = {}

        response = requests.get(url, headers=my_headers, data=payload)

        # Convierte la respuesta JSON en un objeto Python
        response_data = json.loads(response.text)

        # Accede a "totalItems" dentro de "data"
        data = response_data["data"]["data"]
        total_items = response_data["data"]["totalItems"]

        print("total de items", total_items)
        print("url: ", url)
        products = []

        for item in data:
            nombre = item["title"]
            discounted_price = item["discountedPrice"]
            dispresentation = item["presentation"]
            title = dispresentation["title"]
            description = dispresentation["description"]
            presentation = title + description

            product = Product(
                name=nombre,
                presentation=presentation,
                brand=None,
                price_box=None,
                price_blister=None,
                source_information=None,
                lifting_date=None,
                laboratory=None,
                card_discount=f"S/{discounted_price:.2f}",
                crossed_price=None,
                suggested_comment=None
            )

            products.append(product)

        return products
'''


    

    

    


