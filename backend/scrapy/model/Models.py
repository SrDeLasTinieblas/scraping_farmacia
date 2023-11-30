
class Category:
    def __init__(self, title, url):
        # Aveces sera url o id
        self.url = url
        self.title = title  


class Product:
    
        def __init__(self, id_sku, precio1, precio2, nombre_producto, pais_fabricacion, registro_sanitario, condicion_venta, tipo_producto, nombre_titular, nombre_fabricante,
                     presentacion, laboratorio, director_tecnico, nombre_comercial, telefono, direccion, departamento, 
                     provincia, distrito, horario_atencion, ubigeo, cat_codigo, email, ruc, cod_establecimiento):
            self.id_sku = id_sku
            self.precio1 = precio1
            self.precio2 = precio2
            self.nombre_producto = nombre_producto
            self.pais_fabricacion = pais_fabricacion
            self.registro_sanitario = registro_sanitario
            self.condicion_venta = condicion_venta
            self.tipo_producto = tipo_producto
            self.nombre_titular = nombre_titular
            self.nombre_fabricante = nombre_fabricante
            self.presentacion = presentacion
            self.laboratorio = laboratorio
            self.director_tecnico = director_tecnico
            self.nombre_comercial = nombre_comercial
            self.telefono = telefono
            self.direccion = direccion
            self.departamento = departamento
            self.provincia = provincia
            self.distrito = distrito
            self.horario_atencion = horario_atencion
            self.ubigeo = ubigeo
            self.cat_codigo = cat_codigo
            self.email = email
            self.ruc = ruc
            self.cod_establecimiento = cod_establecimiento

        
        """
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
        """  
            
            
           
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
                return f"{self.id_sku}|{self.precio1}|{self.precio2}|{self.nombre_producto}|{self.pais_fabricacion}|{self.registro_sanitario}|{self.condicion_venta}|{self.tipo_producto}|{self.nombre_titular}|{self.nombre_fabricante}|{self.presentacion}|{self.laboratorio}|{self.director_tecnico}|{self.nombre_comercial}|{self.telefono}|{self.direccion}|{self.departamento}|{self.provincia}|{self.distrito}|{self.horario_atencion}|{self.ubigeo}|{self.cat_codigo}|{self.email}|{self.ruc}|{self.cod_establecimiento}"

                
        
'''
        print("\t\t"+self.description)
        print("\tImages:")
        for image in self.images:
            print("\t\t"+ image)
'''
      
        

        
















