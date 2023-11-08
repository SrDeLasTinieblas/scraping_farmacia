from flask import Flask, jsonify
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.BoticasHogarSalud import BoticasHogarSalud
import concurrent.futures
from utils.NetUtils import download_page, get_random_user_agent
import time


app = Flask(__name__)

# Define tus páginas como instancias de clases
boticas_peru = BoticasPeru()
boticas_salud = BoticasSalud()
boticas_hogar_salud = BoticasHogarSalud()

# Función para descargar un producto desde una página específica
def download_product(page, product_url):
    return page.get_product(product_url)

# Función para descargar productos de una página específica
def download_products(page, category_url):
    final_products = []
    product_urls = page.get_product_urls(category_url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_product, page, url): url for url in product_urls}
    for future in concurrent.futures.as_completed(futures):
        product_url = futures[future]
        product = future.result()
        if product is not None:  # Verificar si el producto no es None antes de agregarlo
            final_products.append(product)
    return final_products


# Ruta para descargar un producto
@app.route('/download_product/<page>/<product_url>', methods=['GET'])
def download_product_api(page, product_url):
    page_instance = None
    if page == 'boticas_peru':
        page_instance = boticas_peru
    elif page == 'boticas_salud':
        page_instance = boticas_salud
    elif page == 'boticas_hogar_salud':
        page_instance = boticas_hogar_salud
    if page_instance:
        product = download_product(page_instance, product_url)
        if product:
            return jsonify({product})
    return jsonify({'message': 'Producto no encontrado o error en la descarga'})

# Ruta para descargar productos de una página
@app.route('/download_products/<page>', methods=['GET'])
def download_products_api(page):
    page_instance = None
    if page == 'boticas_peru':
        page_instance = boticas_peru
    elif page == 'boticas_salud':
        page_instance = boticas_salud
    elif page == 'boticas_hogar_salud':
        page_instance = boticas_hogar_salud
    if page_instance:
        # Supongamos que tienes un valor de category_url, reemplaza 'valor_del_category_url' con el valor real
        
        products = download_products(page_instance)  # Utiliza page_instance y category_url
        if products:
            return jsonify({'message': 'Productos descargados exitosamente', 'products': products})
    return jsonify({'message': 'Productos no encontrados o error en la descarga'})

if __name__ == '__main__':
    app.run(debug=True)
