import random
from time import time
from pages.Digemid import Digemid
from utils.UploadDatabase import upload_to_db

"""
    Farmacia Universal  = 1
    Inkafarma           = 2
    Boticas y Salud     = 3
    Boticas Peru        = 4
    Hogar y Salud       = 5
    Digemin             = 6
    
"""


digemid = Digemid()

simbol_concantened = "¬"
products_information_list = []
products_to_send = 1000
total_productos_enviados = 0  
resultados = digemid.obtenerParametros()
products_digimid = []
tiempo_inicial = time()
nombre_de_product = ""

print("Tamaño de productos a obtener:", len(resultados))

if len(resultados) > 0:
    for resultado in resultados:
        print(f"resultado -><- {resultado}")
        nombre_de_product = resultado['PROD_NOMBRE']
        concentracion = resultado['PROD_CONCENTRACION']
        
        key_productos = digemid.step_2(product_name=nombre_de_product, product_concent=concentracion)
        if not key_productos:
            continue
        
        for key_producto in key_productos:
            key_grupo = key_producto["grupo"]
            key_concent = key_producto["concent"]
            key_codGrupoFF = key_producto["codGrupoFF"]  

            products = digemid.step_3(key_group=key_grupo, 
                                    key_concent = key_concent,
                                    nombre_producto=nombre_de_product,
                                    key_codGrupoFF = key_codGrupoFF
                                )
            if not products:
                continue
            
            for product in products:
                if not product:
                    continue
                
                internal_product = digemid.step_4(product)            
                if not internal_product:
                    continue
                products_digimid.append(internal_product)
                
products_text = []
for product in products_digimid:
    products_text.append(product.show_information())

final_products_text = simbol_concantened.join(products_text)
final_products_text_with_prefix = f"6¯{final_products_text}"

total_productos_enviados = len(products_digimid)

upload_to_db(final_products_text_with_prefix)
print(final_products_text_with_prefix)

with open("productos_enviados.txt", "w", encoding="utf-8") as file:
    file.write(final_products_text_with_prefix + "\n")

print(f"Total de productos enviados al final: {total_productos_enviados}")
tiempo_final = time()
tiempo_total = tiempo_final - tiempo_inicial
print("Tiempo total de ejecución: {} segundos".format(tiempo_total))


"""
while True:
    # Recorrer cada categoría y obtener información de productos
    for category in categories:
        product_ids = digemid.get_product_urls(category)
        # Iterar sobre los product_ids y obtener los productos
        for product_id in product_ids:
            products = digemid.get_product(product_id)

            # Verificar si se descargaron productos correctamente
            if products:
                print(f"Se descargaron {len(products)} productos para el ID: {product_id}")
                # Puedes hacer más cosas con la lista de productos si es necesario
            #else:
                #print(f"No se descargaron productos para el ID: {product_id}")
                
            if products is not None and len(products) >= 1:
                print("Tamaño: ", len(products))
                print("product_id: ", len(product_id))
                for product in products:
                    product_more_details = digemid.get_product_more_details(product)
                    if not product_more_details:
                        continue

                    product_information = product_more_details.show_information()

                    # Verificar si la información del producto no es None antes de agregarla a la lista
                    if product_information is not None:
                        products_information_list.append(product_information)
                        products_collected += 1

                        # Verificar si se han recolectado 1000 productos
                        if products_collected % 20 == 0:
                            # Enviar productos a la base de datos en lotes de 50
                            chunks = [products_information_list[i:i + products_to_send] for i in
                                      range(0, len(products_information_list), products_to_send)]

                            for chunk in chunks:
                                final_products_text = simbol_concantened.join(map(str, chunk))
                                final_products_text = f"{digemid.id}¯{final_products_text}{simbol_concantened}"
                                print(final_products_text)
                                upload_to_db(final_products_text)  # Descomenta esta línea cuando estés listo para enviar a la base de datos

                            # Limpiar la lista después de enviar los productos
                            products_information_list = []

# Fin del bucle
"""
 

            
"""
for category in categories:
    product_ids = digemid.get_product_urls(category)

    for product_id in product_ids[:5]:
        products = digemid.get_product(product_id)

        # Verificar si 'products' es None o no es iterable
        if products is None or not isinstance(products, (list, tuple)):
            print(f"Hubo un error al obtener productos para el ID {product_id}")
            continue

        for product in products:
            product_more_detais = digemid.get_product_more_details(product)

            if not product_more_detais:
                continue

            final_products_text = simbol_concantened.join(product_more_detais)
            final_products_text = f"{digemid.id}¯{final_products_text}{simbol_concantened}"
            print(final_products_text)
            upload_to_db(final_products_text)
                    For next call need data
                    codigoProducto":53725,"         ====> codProdE  ====> name
                    codEstablecimiento":"0053974"   ====> codEstab  ====> id_sku
                
      
# For More Datails :V

product = Product(
    id_sku = "0022645",
    name =  53725,
    presentation =  None,
    brand = None,
    price =  None,
    source_information = None,
    lifting_date =  None,
    laboratory =  None,
    card_discount = None,
    crossed_price =  None,
    suggested_comment =  None,
    description=None
)

product_more_detais = digemid.get_product_more_details(product)
#product_more_detais.show_information2()
#print(product_more_detais)
"""


"""
cadena = "6¯37.83|2.70|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|DEXTRE MENACHO FREDY WILDER|FARMACIA DE LA CLINICA INTERNACIONAL S.A.|150130|06|aoyarce@cinternacional.com.pe|20100054184|0089663¬37.83|2.70|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|GUTIERREZ CARHUAMACA FLOR DEL CARMEN|FARMACIA DEL POLICLINICO CENTRO AMBULATORIO CLINICA INTERNACIONAL SEDE-SURCO|150140|06|aoyarce@cinternacional.com.pe|20100054184|0045492¬37.83|2.70|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|VASQUEZ VILLAR IRIS SONALI|FARMACIA DE LA CLINICA INTERNACIONAL|150101|06|aoyarce@cinternacional.com.pe|20100054184|0021037¬37.83|2.70|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|VASQUEZ VILLAR IRIS SONALI|FARMACIA DEL CENTRO MEDICO SAN ISIDRO|150131|06|aoyarce@cinternacional.com.pe|20100054184|0019355¬37.83|2.70|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|VILLARRUEL DOMINGUEZ RUTH MARIA|FARMACIA DE LA CLINICA  INTERNACIONAL S.A.|150101|06|aoyarce@cinternacional.com.pe|20100054184|0014542¬57.40|4.10|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|LUQUE YAHUA ELIZABETH ERIKA GABRIELA|POLICLINICO SOCIAL ALEMAN ESPIRITU SANTO SAN MARTIN DE PORRES|040101|04|farmacia@policlinicosespiritusanto.org|20453914772|0027869¬57.40|4.10|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|ESCOBEDO TUPIA MARIA ROSA|BOTICA DEL POLICLINICO SOCIAL ALEMAN ESPIRITU SANTO ALTO SELVA ALEGRE|040102|04|farmacia@policlinicosespiritusanto.org|20453914772|0072170¬57.86|4.13|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|ALVARADO BONIFACIO DIANA SOFIA|CLINICA CAYETANO HEREDIA|120114|06|farmacia@clinicacayetanoheredia.com|20485947273|0115017¬65.80|4.70|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|QUIROZ DE LA CRUZ ROSARIO ISABEL|FS SOCORRO|120114|04|isladetrank@hotmail.com|20486562341|0047061¬67.20|4.80|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|TAPIA SANCHEZ YERTY MARIBEL|BOTICAS ECONOFARMA|021809|04|econofarma1@hotmail.com|20600023935|0036549¬67.20|4.80|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|YABIKU TERUKINA LUIS ALBERTO|BOTICA CENTRAL|150801|04|hiromifarma@hotmail.com|20601314984|0062709¬68.60|4.90|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|LOPEZ JARAMILLO CYNTHIA|BOTICAS LIANFARMA|021801|04|lianfarma_lam@hotmail.com|20531904649|0110449¬68.60|4.90|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|LOPEZ JARAMILLO CYNTHIA|BOTICAS  LIANFARMA|021809|04|lianfarma_lam@hotmail.com|20531904649|0102143¬68.60|4.90|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|MIÑANO RUIZ ELBERT WILLIAM|BOTICA LIANFARMA|021809|04|lianfarma_central@hotmail.com|20601723086|0050071¬68.60|4.90|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|CHIPANA HUAUYA NORMA MARIBEL|FARMACIA SOLIDARIDAD LOS OLIVOS|150117|06|e.nfarmasac@gmail.com|20600090764|0045702¬68.60|4.90|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|JIMENEZ GONZALES JUAN PABLO|INKAFARMA|200601|04|regulatorio@farmaciasperuanas.pe|20608430301|0025226¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|PARI CHURA ESTHER NOHEMI|BOTICA SAN PEDRO|080101|04|dsanpedrosac@hotmail.com|20490766651|0050998¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|NINAPAYTAN FUENTES MARIA DE GUADALUPE|BOTICA PARAMEDICA|180301|04|ronaldcastellanossalinas@gmail.com|20609710081|0107930¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|FRANCO LASTRERA HENRY|SAN PEDRO|080108|04|dsanpedrosac@hotmail.com|20490766651|0071711¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|HERRERA ARREATEGUI ANA MARIA|BOTICA FARMAVIDA|130101|04|inversionesfarmavida@gmail.com|20481472831|0052103¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|CABRERA ORMEÑO FELIX ORLANDO|BOTICA FARMADER|080101|04|boticaenmanuel.lc@gmail.com|10239269155|0071188¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|ARIAS BARRON JHANNA ROSS|BOTICA FALCON|100101|04|delifar2008@hotmail.com|20573281005|0069230¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|ZAPATA IBARRA MARCELO DAVID|ARCANGEL LEON|200701|06|consultorioarcangel.leon@gmail.com|20530277098|0081113¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|ALDANA MARTINEZ VICTOR RAUL|CADENAS 24 HORAS|200401|04|henry.sistemas@cadenas24horas.com|20484204439|0109522¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|RAMIREZ AQUINO LUIS ALBERTO|BOTICA 24 HORAS|200602|04|henry.sistemas@cadenas24horas.com|20484204439|0028570¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|VALDERRAMA CASTAÑEDA EDWARD ALBERTO|CADENA 24 HORAS S.A.C.|200601|03|henry.sistemas@cadenas24horas.com|20484204439|0028557¬70.00|5.00|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|GARCIA DIAZ LILIANA ESTELA|BOTICA  24 HORAS|200401|04|henry.sistemas@cadenas24horas.com|20484204439|0025144¬70.70|5.05|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|BRUNO REYES MARIA ANGELICA|BOTICAS MIFARMA|200601|04|regulatorio@farmaciasperuanas.pe|20512002090|0098977¬70.70|5.05|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|DELGADO NUÑEZ ROCIO DEL PILAR|CORPORACION FASUR PERU|040101|03|farmaciafasurperu@gmail.com|20498176144|0020515¬70.70|5.05|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|ESTRADA ZAMBRANO ELIANA ROSARIO|CORPORACION FASURPERU|040126|03|farmaciafasurperu@gmail.com|20498176144|0072754¬70.70|5.05|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|FIGUEROA CABALLERO SUGHEY MARLITH|FARMACIA  CORPORACION FASUR PERU|040129|03|farmaciafasurperu@gmail.com|20498176144|0040450¬70.70|5.05|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|GAMERO PAREDES LUCIA ELSA|FARMACIA CORPORACION FASURPERU IV|040103|03|farmaciafasurperu@gmail.com|20498176144|0027577¬71.40|5.10|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|FLORES CASTAÑEDA ANGELA PATRICIA|BOTICA FARMAX|130101|04|direcciontecnica@drogueriafarmaxsac.com|20600144635|0054109¬71.84|5.13|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|CHAVARRIA CHANG CARMEN DEL PILAR|BOTICA BOTICAS VIDA|150801|04|boticavida_2010@hotmail.com|20517713385|0062061¬72.80|5.20|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|PASCUAL DIESTRA SELMA ISABEL|BOTICA MODERNA|150135|04|danton@moderna.com.pe|20505579799|0040162¬74.20|5.30|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|DEL ALAMO CAMPOS PATRICIA|BOTICA JUANITA S.R.L.|080108|04|nemeca125@hotmail.com|20490853384|0071434¬74.20|5.30|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|HUAMANI PACHECO FIDELIA MARGARITA|BOTICA EFREND|110101|04|boticas_efrend@hotmail.com|10214462481|0068082¬74.20|5.30|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|HUAMANI HINOSTROZA HERMINIO ELVIS|FARMACIA EFREND|110101|03|boticas_efrend@hotmail.com|10214462481|0015419¬74.20|5.30|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|CASTILLO CASTRO EVELIN NAYUT|BOTICAS ECONOFARMA|021801|04|econofarma1@hotmail.com|20600023935|0104302¬74.20|5.30|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|CHAVEZ VILCHERRES KAREN ALICIA|BOTICAS  ECONOFARMA|021801|04|econofarma1@hotmail.com|20600023935|0048852¬74.30|5.31|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|LIÑAN DE LA CRUZ ERICKA LINEYRA|FARMACIA ISIS|130101|03|farmaciaisis@hotmail.com|20477194886|0047117¬75.00|5.36|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|FERNANDEZ CHOQUEHUANCA EDUARD|BOTICA IRENE|150108|04|apusuyosac@hotmail.com|20557554425|0092368¬75.00|5.40|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|AZABACHE GUARNIZ MARIA ROSA|BOTICA LA LIBERTAD|130101|04|EUDENGAR@GMAIL.COM|20600146743|0105529¬76.16|5.44|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|RAFAILE CASTILLO SHIRLEY EVELYN|FARMACIA SANTA FLORENCIA|150136|03|farmasantaflorencia@gmail.com|20605831436|0048825¬76.16|5.44|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|APAZA ALARCON JHOSILEYNI LISBETH|CLINICA ANGLOAMERICANA|150131|04|japaza@angloamericana.com.pe|20107695584|0040849¬77.00|5.50|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|MUÑOZ PARIGUANA GRACIA KATHERINE|ABC FARMA|180301|04|cristhian_fm11@hotmail.com|20604846308|0044686¬77.00|5.50|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|GARCIA SEBASTIAN GABRIELA ELENA|BOTICA PARROQUIAL SAN GABRIEL|150143|04|lenna0905@hotmail.com|20198278107|0085382¬77.00|5.50|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|GEJAÑO GASTELU NELLY EUSEBIA|BOTICA BALANI|150101|04|boticabalani1@hotmail.com|20331714632|0012454¬77.00|5.50|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE||FARMACIA   BAZAN|021808|03|bazan.contabilidad@hotmail.com|10329704390|0099150¬77.00|5.50|XUMER 90  mg|90  mg|Argentina|EE04992|Con receta medica|Marca|TECNOFARMA S.A.|MONTE|Caja Envase Blíster Comprimidos|MONTE|TORRES ALBARRAN MARILIN|FARMACIA  BAZAN|021809|03|bazan.contabilidad@hotmail.com|10329704390|0047847"

"""

