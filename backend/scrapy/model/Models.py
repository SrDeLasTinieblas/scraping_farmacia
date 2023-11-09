
class Product:
        def __init__(self, id_botica, id_sku, name, presentation, brand, price_box, price_blister, source_information, lifting_date, laboratory, card_discount, crossed_price, suggested_comment):
            self.id_botica = id_botica
            self.id_sku = id_sku
            self.name = name
            self.presentation = presentation
            self.brand = brand
            self.price_box = price_box
            self.price_blister = price_blister
            self.source_information = source_information
            self.lifting_date = lifting_date
            self.laboratory = laboratory
            self.card_discount = card_discount
            self.crossed_price = crossed_price
            self.suggested_comment = suggested_comment
            
        def show_information(self):
                
                print("Product Information:")
                print(f"\tSKU: {self.id_botica}")
                print(f"\tSKU: {self.id_sku}")
                print(f"\tName: {self.name}")
                print(f"\tPresentation: {self.presentation}")
                print(f"\tBrand: {self.brand}")
                print(f"\tPrice Box: {self.price_box}")
                print(f"\tPrice Blister: {self.price_blister}")
                print(f"\tSource Information: {self.source_information}")
                print(f"\tLifting Date: {self.lifting_date}")
                print(f"\tLaboratory: {self.laboratory}")
                print(f"\tCard Discount: {self.card_discount}")
                print(f"\tCrossed Price: {self.crossed_price}")
                print(f"\tSuggested Comment: {self.suggested_comment}")
                print("-" * 20)
        
        

        
        
'''
        print("\t\t"+self.description)
        print("\tImages:")
        for image in self.images:
            print("\t\t"+ image)
'''
      
        

        
















