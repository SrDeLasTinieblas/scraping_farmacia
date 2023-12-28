import json
import re
from model.Models import Product
from pages.base.base import Page
from utils.NetUtils import download_json

class BaseResponseFarma(Page):
    
    code_farma = None
    code_company = None
    
    def __init__(self, id = None, title = None, url = None):
        super().__init__(id, title, url)
        self.name = title  # Agregar el atributo 'name'

    """
    def get_categories(self):        
        categorys = {}        
        category_url = f"https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/{self.code_farma}/departments?companyCode={self.code_company}&saleChannel=WEB&saleChannelType=DIGITAL&sourceDevice=null"
        data = download_json(category_url)
                
        for item in data:   
            category_id = item["id"]
            category_name = item["name"]
            categorys[category_id] = category_name
            #categorys.append(item["id"])                              
                           
        return categorys
    """
    
    def get_categories(self):        
        categories = []        
        category_url = f"https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/{self.code_farma}/departments?companyCode={self.code_company}&saleChannel=WEB&saleChannelType=DIGITAL&sourceDevice=null"
        data = download_json(category_url)
                
        for item in data:   
            category_id = item["id"]
            category_name = item["name"]
            #categories.append({"id": category_id, "name": category_name})
            categories.append({"id": category_id, "name": category_name})

        #print("category_url: ", category_url)        
        #print("categories: ", categories)              
        return categories

    
    def get_product_urls(self, category_id):
        
        #url = f"https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/{self.code_farma}/filtered-products?companyCode={self.code_company}&saleChannel=WEB&saleChannelType=DIGITAL&sourceDevice=null"
        url = f"https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/{self.code_farma}/filtered-products?companyCode={self.code_company}&saleChannel=WEB&saleChannelType=DIGITAL&sourceDevice=null"
        
        payload = json.dumps({
            "departmentsFilter": [
                category_id["id"]
            ],
            "categoriesFilter":[ ],
            "subcategoriesFilter":[],
            "brandsFilter":[],
            "ranking":"null",
            "page":0,
            "rows":2000,
            "order":"ASC",
            "sort": "ranking",
            "productsFilter": [ ]
            })
        
            #print("post::.", post_url)
            
        headers = {
            
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'AndroidVersion': '100000',
            #'x-access-token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0OWU0N2ZiZGQ0ZWUyNDE0Nzk2ZDhlMDhjZWY2YjU1ZDA3MDRlNGQiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9taWZhcm1hLXByb2QiLCJhdWQiOiJtaWZhcm1hLXByb2QiLCJhdXRoX3RpbWUiOjE2OTUxNTYyNTEsInVzZXJfaWQiOiJGUENWOHQ3WjM1UzBzc2dGbkVoNHFsbWdRSUQzIiwic3ViIjoiRlBDVjh0N1ozNVMwc3NnRm5FaDRxbG1nUUlEMyIsImlhdCI6MTY5OTQxNDcyOSwiZXhwIjoxNjk5NDE4MzI5LCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImFub255bW91cyJ9fQ.ZHcA_00XchZwSpyPnMrSuJnVa4GDmu37lA-ST4hE_1es7fYlew2F9QpAawP90MWTzumzPB5zzygEpOQA4NWmExVxtjZaBNFMfWZdUrkMMSn900Ec2TlTg4nZMAuzdB01ED6OsFCEDhGGjrHG3bd6OqWDDAbte0fbAfSOOJFLjmwzCLfVjq3ilxNy59M32QyGNAkd381O7BtfOGd1HFxBs8Tv2wL6fyZGZYw4T_rm48HqulmRcAo7JZDqPZlqndRYBx9xTeAo_qBcXjZqnl-GnHw2LmKn3JmgtaD2CjFb_lna1x8htdOv4Kj3gopo_iEN90EQsCkUYdHzRQ80-lqHDw',
            'drugstore-stock': '1253',
            'Content-Type': 'application/json',
            'Origin': f"{self.url}",
            'Connection': 'keep-alive',
            'Referer': f"{self.url}/",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }
                    
        # Realizar la primera petición
        response_data = download_json(url=url, method="POST", headers=headers, data=payload)
        
        try:
            total = response_data.get("total", 0)
            products_id_row = []

            # Realizar las solicitudes adicionales según el valor de "total"
            for _ in range(total):
                # Realizar la solicitud
                response_data = download_json(url=url, method="POST", headers=headers, data=payload)
                if response_data is None:
                    print("La respuesta es None. Saltando a la siguiente iteración.")
                    continue

                rows = response_data.get("rows", [])
                for row in rows:
                    id_row = row.get("id")
                    name = row.get("name")
                    if name:
                        products_id_row.append(id_row)

            return products_id_row
        
        except Exception as e: 
            print(f"{self.title} : Hubo un error al extraer datos en {category_id} -> {str(e)}")      

        return None
             
                    
                              
    def get_product(self, product_id):
        
        product_url = f"https://5doa19p9r7.execute-api.us-east-1.amazonaws.com/{self.code_farma}/product/{product_id}?companyCode={self.code_company}&saleChannel=WEB&saleChannelType=DIGITAL&sourceDevice=null"
        json = download_json(product_url)
        if not json:
            #print(f"{self.title} : Hubo un error al descargar el producto = {product_url}")
            return None
            
        products = []    
            
        try:
            
            """
                response Json
                
                {
                    "id": "011592",
                    "name": "Gel Hidratante Facial Hydro Boost Neutrogena - Pote 50 G",
                    "brand": "NEUTROGENA",
                    "price": 55.5,
                    "fractionatedPrice": 0,
                    "presentation": "POTE",
                    "quantityUnits": 1,
                    "unitMeasure": "G",
                    "fractionalMode": false,
                    "activePrinciples": null,
                    "fractionatedForm": null,
                    "fractionatedText": null,
                    "noFractionatedText": "POTE 50 G",
                    "productStatusId": 1,
                    "productStatus": "AVAILABLE",
                    "productStatusMessage": null,
                    "maxUnitSale": 6,
                    "maxUnitSaleFractionated": 0,
                    "stock": 342,
                    "fractionalStock": 0,
                    "stockRet": 342,
                    "fractionalRetStock": 0,
                    "showStockAlert": "N",
                    "fractionatedSelected": null,
                    "unitPriceSelected": null,
                    "quantitySelected": 0,
                    "subTotal": null,
                    "fractionalCore": false,
                    "quantityUnitsCore": 1,
                    "limitOfferTime": null,
                    "slug": "gel-hidratante-facial-hydro-boost-neutrogena",
                    "skuVariants": [],
                    "presentationIdSelected": null,
                    "fractionatedPresentationId": null,
                    "presentationId": 1,
                    "quantityUnitsFractionated": null,
                    "visiblePresentations": [
                        "pack"
                    ],
                    "pricePack": 55.5,
                    "quantityUnitsPack": 1,
                    "unitPrice": 0,
                    "tagImageUrl": "",
                    "secondaryTagImageUrl": null,
                    "alertTagText": "",
                    "priceAllPaymentMethod": 41.5,
                    "fractionatedPriceAllPaymentMethod": 0,
                    "priceWithpaymentMethod": 37.3,
                    "fractionatedPriceWithpaymentMethod": 0,
                    "crossOutPL": true,
                    "crossOutFractionatedPL": false,
                    "paymentMethodCardType": "1",
                    "unitPriceAllPaymentMethod": 0,
                    "unitPriceWithPaymentMethod": 0,
                    "subTotalAllPaymentMethod": null,
                    "subTotalWithPaymentMethod": null,
                    "isFromSeller": false,
                    "sellerId": null,
                    "sellerName": null,
                    "ranking": 94,
                    "itemsPack": null,
                    "totalAmountComponentPack": null,
                    "productPack": false,
                    "guaranteed": "GP",
                    "skuMifarma": "558606",
                    "publishWithoutStock": true,
                    "priceTmpFromSellerCenter": false,
                    "isUnitPresentationDefault": false
                    }
                
            """
            name = json["name"]
            price = float(json["price"])
            sku_mifarma = json["skuMifarma"]
            brand = json["brand"]
            price_with_payment_method = float(json["priceWithpaymentMethod"])     
            price_all_payment_method = float(json["priceAllPaymentMethod"])
            fractionated_price = json["fractionatedPrice"]
            fractionated_form = json["fractionatedForm"]
            
            presentacion = json["presentation"]
                        
            #palabras_clave = ['ml', ' ml', ' gramos', 'gramos', 'mg', ' mg', 'un', ' un']
            palabras_clave = ['ml', ' ml', ' gramos', 'gramos', 'mg', ' mg']
            
            
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
                primer_valor_mg_values = 0
                palabra = ''
                
                
                
            product = Product(
                id_sku = sku_mifarma,
                name =  name,
                concentracion = str(primer_valor_mg_values) + palabra,
                presentation =  f"{presentacion}",
                brand = brand,
                price =  f"{price:.2f}",
                source_information =  self.title,
                lifting_date =  None,
                laboratory =  None,
                card_discount = f"{price_all_payment_method}",
                crossed_price =  None,
                suggested_comment =  None,
                description=None
            )
            
            products.append(product)
                
             
        except Exception as e:
            print(f"{self.title} : Hubo un error al extraer datos en {product_url} -> {str(e)}")      
    
        return products if products else None