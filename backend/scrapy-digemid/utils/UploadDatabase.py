import random
import time
import traceback
import pyodbc


def upload_to_db(text_upload):
    
    """
    server = '154.53.44.5\SQLEXPRESS'
    database = 'BDCOMPRESOFT'
    username = 'userTecnofarma'
    password = 'Tecn0farm@3102'
    
    
    server = 'DESKTOP-N5GCHST\SQLEXPRESS'
    database = 'farmacia'
    username = ''
    password = ''
    
    
    """
    

    
    server = '154.53.44.5\SQLEXPRESS'
    database = 'BDCOMPRESOFT'
    username = 'userTecnofarma'
    password = 'Tecn0farm@3102'
    
    
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        text_upload = f'{text_upload}'
        cursor.execute("{CALL uspOperacionesMovimientosImportarDIGEMIDCSV (?)}", (text_upload))

        conn.commit()
        conn.close()

        return True 
    except Exception as e:
        print(f"Error al cargar en la base de datos: {str(e)}")
        traceback.print_exc()
        return False
    
    
    
        '''
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("{CALL uspOperacionesMovimientosImportarCSV (?)}", (text_upload))
        conn.commit()
        conn.close()

        return True 
    except Exception as e:
        print(f"Error al cargar en la base de datos: {str(e)}")
        traceback.print_exc()
        return False
    
        '''
        
        '''
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
        '''









