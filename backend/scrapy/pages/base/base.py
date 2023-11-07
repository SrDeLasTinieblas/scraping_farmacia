
class Page:
    def __init__(self, title, url):
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
        # Toma una categoria -> Devuelve otra de links de productos
        """
            ["https://boticasperu.pe/product_1", "https://boticasperu.pe/product_2" ]
        """
        pass
        
    def get_product(self, product):
        # Toma un objeto Product y devuelve detalles específicos
        pass
    
    