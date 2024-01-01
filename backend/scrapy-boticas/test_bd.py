import re
import json

json_string = """{
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "Tensiómetro de Brazo 08C Contec x 1 Un",
    "image": "assets/sources/Hero Image/HERO%20IMAGES%20(4).jpg",
    "description": "
        Medida de la presi&oacute;n arterial completamente autom&aacute;tica.
        Almacena los resultados de las medidas de tres usuarios y hasta 99 elementos para cada usuario. Libre para cambiar, f&aacute;cil de usar.
        Muestra datos de medida con LCD digital de fuente grande. Los datos NIBP son claros de un vistazo.
        Suministre dos tipos de unidades de medida NIBP: mmHg / kPa. Seg&uacute;n el h&aacute;bito de cambiar.
        Con funci&oacute;n de apagado autom&aacute;tico. El dispositivo se apagar&aacute; autom&aacute;ticamente cuando no haya operaci&oacute;n durante un tiempo prolongado (m&aacute;s de 5 minutos) o cuando haya poca energ&iacute;a.
        RS: DB5959E
    ", 
    "sku": "24207",
    "offers": {
        "@type": "Offer",
        "url": "https://farmaciauniversal.com/producto/detalle/2795-tensiometro-de-brazo-08c-contec-x-1-un",
        "priceCurrency": "PEN",
        "price": "267.61"
    }
}"""

# Utilizar expresiones regulares para eliminar caracteres especiales
#cleaned_json_string = re.sub(r'[^a-zA-Z0-9{}":,./\-_ ]', '', json_string)


cleaned_json_string = """{
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "Jalk Miel de Abeja x 1 kg",
    "image": "assets/sources/PRODUCTOS/Miel20de20abeja20Jalk20-20120kg20-200936520-20Farmacia20Universal.jpg",
    "description": "La miel es una sustancia dulce natural producida por las abejas a partir del neacutectar de plantas o de secreciones de partes vivas de las plantas o de excreciones de insectosnbspchupadores presentes en las partes vivas de las plantas, que las abejas recolectan, transforman combinaacutendolas con sustancias especiacuteficas de las propias, depositan,nbspdeshidratan, almacenan y las dejan en las colmenas para que madure Codex Alimentarius. Este producto es valorado por sus propiedades nutricionales, medicinales y terapeacuteuticas.RS:nbspF6005520N - NADSJL",
    "sku": "09365",
    "offers": {
        "@type": "Offer",
        "url": "https://farmaciauniversal.com/producto/detalle/3524-jalk-miel-de-abeja-x-1-kg",
        "priceCurrency": "PEN",
        "price": "52.90"
    }
}"""


cleaned_json_string2 = """
                {
                "@context": "https://schema.org/", 
                "@type": "Product", 
                "name": "Jalk Miel de Abeja x 1 kg",
                "image": "assets/sources/PRODUCTOS/Miel%20de%20abeja%20Jalk%20-%201%20kg%20-%2009365%20-%20Farmacia%20Universal.jpg",
                "description": "La miel es una sustancia dulce natural producida por las abejas a partir del n&eacute;ctar de plantas o de secreciones de partes vivas de las plantas o de excreciones de insectos&nbsp;chupadores presentes en las partes vivas de las plantas, que las abejas recolectan, transforman combin&aacute;ndolas con sustancias espec&iacute;ficas de las propias, depositan,&nbsp;deshidratan, almacenan y las dejan en las colmenas para que madure "(Codex Alimentarius). Este producto es valorado por sus propiedades nutricionales, medicinales y terap&eacute;uticas.RS:&nbsp;F6005520N - NADSJL", 
                "sku": "09365",
                "offers": {
                "@type": "Offer",
                "url": "https://farmaciauniversal.com/producto/detalle/3524-jalk-miel-de-abeja-x-1-kg",
                "priceCurrency": "PEN",
                "price": "52.90"
                }
                }
"""


# Utilizar expresiones regulares para extraer el valor del campo "sku"
match = re.search(r'"sku":\s*"([^"]+)"', json_string)
if match:
    sku_value = match.group(1)
    print(f"SKU encontrado: {sku_value}")
else:
    print("SKU no encontrado en la cadena JSON.")
    
    
    
    
    
    