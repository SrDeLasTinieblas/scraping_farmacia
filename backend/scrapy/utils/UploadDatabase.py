import random
import time
from pages.BoticasPeru import BoticasPeru
from pages.BoticasSalud import BoticasSalud
from pages.HogarSalud import HogarSalud
from pages.FarmaUniversal import FarmaUniversal
import pyodbc


def upload_to_db(text_upload):
    """
    server = '154.53.44.5\SQLEXPRESS'
    database = 'testEmpresa'
    username = 'userTecnofarma'
    password = 'Tecn0farm@3102'
    """

    server = 'tinieblaserver.database.windows.net'
    database = 'testEmpresa'
    username = 'FacturacionInventario'
    password = 'Darkangelo2023'

    # Crea una cadena de conexión
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Establece la conexión
    conn = pyodbc.connect(conn_str)

    # Crea un cursor
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO productos (productos)
    VALUES (?)
    """
    cursor.execute(insert_query, text_upload)
    conn.commit()

    # Cierra el cursor y la conexión
    cursor.close()
    conn.close()



