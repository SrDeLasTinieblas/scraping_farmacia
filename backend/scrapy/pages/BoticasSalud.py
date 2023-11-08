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
        
        if not response_data:
            print(f"{self.title} : Hubo un error al descargar el producto = {product_slug}")
            return None
        
        try:    

            item = response_data["data"] 
            title = item["title"]
            discounted_price = item["discountedPrice"]
            dispresentation = item["presentations"][0]
            
            title_presentation = dispresentation["title"]
            description = dispresentation["description"]
            normal_price = dispresentation["price"]
            presentation = title_presentation + description
            product_brand = item["productBrand"]
            brand = product_brand["title"]
            
            # laboratorio = None   
            #for details in item["details"]:
            #    if details["name"] == "Laboratorio":
            #       laboratorio = details["description"]
                
            laboratorio = next((details["description"] for details in item["details"] if details["name"] == "Laboratorio"), None)

            #if laboratorio is not None:
                #print(laboratorio)
            
            product = Product(
                name = title,
                presentation= title_presentation,
                brand = brand,
                price_box= None,
                price_blister = f"S/{normal_price:.2f}",
                source_information = self.title,
                lifting_date = None,
                laboratory = laboratorio,
                card_discount = f"S/{discounted_price:.2f}",
                crossed_price = None,
                suggested_comment = None
            )
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {product_slug} -> {str(e)}")          
            
            
        return product
    
    
    

    

    

    


