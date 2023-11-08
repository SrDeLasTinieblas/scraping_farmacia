
from bs4 import BeautifulSoup
from utils.NetUtils import download_json, download_page


class Page:
    def __init__(self, title = None, url = None):
        if title is None:
            raise ValueError("El título debe definirse")
        if url is None:
            raise ValueError("La URL debe definirse")
        
        self.title = title
        self.url = url

    def get_categories(self):
        # Devuelve una lista String - Categorias
        # Ejemplo :::: 
        """
            ['https://boticasperu.pe/promociones.html', 'https://boticasperu.pe/bienestar-sexual.html']
        """        
        pass
    
    
    def get_product_urls(self, category_url):
        html = download_page(category_url)
        if not html:
            print(f"{self.title} : Hubo un error al descargar el category = {category_url}")
            return None

        product_urls = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
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
           
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return product
    
    