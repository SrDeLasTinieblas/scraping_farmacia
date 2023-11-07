from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_page

class Botica(Page):
    
    def __init__(self, title, url):
        super().__init__(title, url)

    def get_categories(self):        
        categorys = []     
        return categorys
    
    
    def get_product_urls(self, category_url):
        product_urls = []
        return product_urls    
                    
                            
    def get_product(self, url_product):
        # Simulación: Toma un objeto Product y devuelve detalles específicos
        return url_product