import json
from model.Models import Product
from pages.base.base import Page
from bs4 import BeautifulSoup
from utils.NetUtils import download_json, download_json_categorias, download_page, get_random_user_agent

class Mifarma(Page):
     
    def __init__(self, title = "Mi farma", url = "https://www.mifarma.com.pe/"):
        super().__init__(title, url)


    def collect_categories(self):
        url = "https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/MMMFPRD/departments?companyCode=MF&saleChannel=WEB&saleChannelType=DIGITAL&sourceDevice=null"
        response_data = download_json_categorias(url)
        categories = response_data
        
        if not response_data:
            print(f"{self.title} : Hubo un error al descargar category = ")
            return None
        
        categories_list = []
        id_list = []
        categorias_url = []

        for category in categories:
            keyword = category.get("keyword")  # Obtener el keyword del elemento principal
            id_producto = category.get("id")  # Obtener el keyword del elemento principal

            categorias_url.append(f"https://www.mifarma.com.pe/categoria/{keyword}")
            
            id_list.append(id_producto)

        return categorias_url, id_list #, 

    
    def get_product_urls(self, categoria_id):
        
        url = "https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/MMMFPRD/filtered-products?companyCode=MF&saleChannel=WEB&saleChannelType=DIGITAL&sourceDevice=null"
        
        payload = json.dumps({
            "departmentsFilter": [
                categoria_id
            ],
            "categoriesFilter": [],
            "subcategoriesFilter": [],
            "brandsFilter": [],
            "ranking": None,
            "page": 0,
            "rows": 135,
            "order": "ASC",
            "sort": "ranking",
            "productsFilter": []
            })
        
            #print("post::.", post_url)
            
        headers = {
            
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'AndroidVersion': '100000',
            'x-access-token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0OWU0N2ZiZGQ0ZWUyNDE0Nzk2ZDhlMDhjZWY2YjU1ZDA3MDRlNGQiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9taWZhcm1hLXByb2QiLCJhdWQiOiJtaWZhcm1hLXByb2QiLCJhdXRoX3RpbWUiOjE2OTUxNTYyNTEsInVzZXJfaWQiOiJGUENWOHQ3WjM1UzBzc2dGbkVoNHFsbWdRSUQzIiwic3ViIjoiRlBDVjh0N1ozNVMwc3NnRm5FaDRxbG1nUUlEMyIsImlhdCI6MTY5OTQxNDcyOSwiZXhwIjoxNjk5NDE4MzI5LCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImFub255bW91cyJ9fQ.ZHcA_00XchZwSpyPnMrSuJnVa4GDmu37lA-ST4hE_1es7fYlew2F9QpAawP90MWTzumzPB5zzygEpOQA4NWmExVxtjZaBNFMfWZdUrkMMSn900Ec2TlTg4nZMAuzdB01ED6OsFCEDhGGjrHG3bd6OqWDDAbte0fbAfSOOJFLjmwzCLfVjq3ilxNy59M32QyGNAkd381O7BtfOGd1HFxBs8Tv2wL6fyZGZYw4T_rm48HqulmRcAo7JZDqPZlqndRYBx9xTeAo_qBcXjZqnl-GnHw2LmKn3JmgtaD2CjFb_lna1x8htdOv4Kj3gopo_iEN90EQsCkUYdHzRQ80-lqHDw',
            'drugstore-stock': '1253',
            'Content-Type': 'application/json',
            'Origin': 'https://www.mifarma.com.pe',
            'Connection': 'keep-alive',
            'Referer': 'https://www.mifarma.com.pe/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }
                    
        response_data = download_json(url = url, method="POST", headers=headers, data=payload)
            
        print("response: ", response_data)
        
        #if not response_data:
         #   print(f"{self.title} : Hubo un error al descargar producto = ")
          #  return None
        
        products_name = []
        products_id_row = []
        rows = response_data["rows"]#["data"]
        #print("rows: ", rows)
        for row in rows:
            id_row = row["id"]
            name = row["name"]
            if name:
                products_id_row.append(id_row)             
                products_name.append(name)             
            
        return products_name    
              
              


    def get_product(self, url_product):
        product = None
        
        html = download_page(url_product)
        if not html:
            print(f"{self.title} : Hubo un error al descargar el producto = {url_product}")
            return None
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
        
            title_text = soup.find('h1', class_='page-title').text.strip()
            
            product_info = {}  # Crear un diccionario para almacenar la información
            
            table = soup.find('tbody')
            
            if table:
                rows = table.find_all('tr')
                
                for row in rows:
                    header_cell = row.find('th', class_='col label')
                    data_cell = row.find('td', class_='col data')
                    
                    if header_cell and data_cell:
                        header_text = header_cell.text.strip()
                        data_text = data_cell.text.strip()
                        
                        product_info[header_text] = data_text
                        laboratorio = product_info.get('Laboratorio', None)

            
            script_elements = soup.find_all('script', type='text/x-magento-init')
            target_json = None

            for script_element in script_elements:
                script_content = script_element.string
                data = json.loads(script_content)

                if "Magento_Catalog/js/product/view/provider" in script_content:
                    target_json = data["*"]["Magento_Catalog/js/product/view/provider"]
                    break

            if target_json:
                first_item = list(target_json["data"]["items"].values())[0]
                nombre = first_item.get("images")
                name = nombre[0]["label"]

                prices_info = first_item.get("price_info")
                final_price = prices_info["final_price"]
                regular_price = prices_info["regular_price"]
                
                product = Product(
                    name =  name,
                    presentation =  None,
                    brand =  None,
                    price_box =  f"S/{final_price:.2f}",
                    price_blister =  f"S/{regular_price:.2f}",
                    source_information =  None,
                    lifting_date =  None,
                    laboratory =  laboratorio,
                    card_discount =  None,
                    crossed_price =  f"S/{regular_price:.2f}",
                    suggested_comment =  None
                )
                

            else:
                print("Elemento <script> no encontrado")    
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {url_product} -> {str(e)}")      
    
        return product
    
    

    

    

    

