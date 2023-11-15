
class Category:
    def __init__(self, title, url):
        # Aveces sera url o id
        self.url = url
        self.title = title  


class Product:
        def __init__(self, id_sku, name, presentation, brand, price, source_information, lifting_date, laboratory, card_discount, crossed_price, suggested_comment, description):
            self.id_sku = id_sku
            self.name = name
            self.presentation = presentation
            self.brand = brand
            self.price = price
            self.source_information = source_information
            self.lifting_date = lifting_date
            self.laboratory = laboratory
            self.card_discount = card_discount
            self.crossed_price = crossed_price
            self.suggested_comment = suggested_comment
            self.description = description
            
           
        def show_information2(self):
                print("Product Information:")
                print(f"\tSKU: {self.id_sku}")
                print(f"\tName: {self.name}")
                print(f"\tPresentation: {self.presentation}")
                print(f"\tBrand: {self.brand}")
                print(f"\tPrice: {self.price}")
                print(f"\tSource Information: {self.source_information}")
                print(f"\tLifting Date: {self.lifting_date}")
                print(f"\tLaboratory: {self.laboratory}")
                print(f"\tCard Discount: {self.card_discount}")
                print(f"\tCrossed Price: {self.crossed_price}")
                print(f"\tSuggested Comment: {self.suggested_comment}")
                print(f"\tDesciption: {self.description}")
                print("-" * 20)
        
        
        def show_information(self):
            # Convierte el objeto Product a una cadena en el formato deseado
            return f"{self.id_sku}|{self.name}|{self.presentation}|{self.brand}|{self.price}|{self.laboratory}|{self.card_discount}|{self.crossed_price}|{self.suggested_comment}|{self.lifting_date}|{self.description}|{self.source_information}"


        
        
'''
        print("\t\t"+self.description)
        print("\tImages:")
        for image in self.images:
            print("\t\t"+ image)
'''
      
        

        
















