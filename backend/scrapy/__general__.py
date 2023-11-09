
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.BoticasHogarSalud import BoticasHogarSalud


boticas = [
    BoticasSalud("Boticas y Salud", "https://www.boticasysalud.com"),
    BoticasPeru("Boticas Peru", "https://boticasperu.pe"), 
    BoticasHogarSalud("Hogar y Salud", "https://www.hogarysalud.com.pe")    
]

for botica in boticas:
    categories = botica.get_categories()
    print(f"Botica {botica.title} \n \tCategorias {categories}" )
    print("\n\n")