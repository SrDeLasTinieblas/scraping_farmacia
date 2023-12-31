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
cleaned_json_string = re.sub(r'[^a-zA-Z0-9{}":,./\-_ ]', '', json_string)

json_data = json.loads(cleaned_json_string)

# Imprimir la cadena JSON limpia
print(json_data['sku'])
