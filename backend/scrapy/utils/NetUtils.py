import os
import random
import requests
import json


def get_random_user_agentFix():
    file_ua = "user-agent.txt"
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta del archivo actual

    try:
        file_path = os.path.join(current_directory, file_ua)  # Combina la ruta del archivo actual con el nombre del archivo
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                random_line = random.choice(lines).strip()
                return random_line, file_path  # Devuelve la línea aleatoria y la ruta del archivo
            else:
                return "El archivo está vacío.", file_path
    except FileNotFoundError:
        return "El archivo no existe.", file_path


def get_random_user_agent():        
    random_user_agent, file_path = get_random_user_agentFix()
    return random_user_agent
    
    
    
def download_page(url):
    try:
        user_agent = get_random_user_agent()
        my_headers = {
            "User-Agent": user_agent            
        }
        response = requests.get(url, headers = my_headers)
        if response.status_code != 200:
            return None
         
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la página: {e}")
        return None  
    

def download_json(url, method = "GET", headers = {}, data = {}):
    try:
        user_agent = get_random_user_agent()
        my_headers = {
            "User-Agent": user_agent        
        }      
        if headers:
            my_headers.update(headers)  
                                 
        my_payload = {}   
        if not my_payload:
           my_payload = data  
        else:
            my_payload.update(data)     

        response = requests.request(method = method, url = url, headers=my_headers, data=my_payload)   
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la página {url} : {e}")
        return None    
    
  
def download_json_categorias(url, method = "GET", headers = {}, data = {}):
    try:
        user_agent = get_random_user_agent()
        
        my_headers = {
            "User-Agent": user_agent,
        }      
        if headers:
            my_headers.update(headers)  
                                 
        my_payload = {}   
        if not my_payload:
           my_payload = data  
        else:
            my_payload.update(data)     

        response = requests.request(method = method, url = url, headers=my_headers, data=my_payload)   
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la página {url} : {e}")
        return None    
    

def download_json_mifarma_productos(url, method = "GET", headers = {}, data = {}):
    try:
        user_agent = get_random_user_agent()
        
        my_headers = {
            "User-Agent": user_agent,
              'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'AndroidVersion': '100000',
            'x-access-token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0OWU0N2ZiZGQ0ZWUyNDE0Nzk2ZDhlMDhjZWY2YjU1ZDA3MDRlNGQiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9taWZhcm1hLXByb2QiLCJhdWQiOiJtaWZhcm1hLXByb2QiLCJhdXRoX3RpbWUiOjE2OTUxNTYyNTEsInVzZXJfaWQiOiJGUENWOHQ3WjM1UzBzc2dGbkVoNHFsbWdRSUQzIiwic3ViIjoiRlBDVjh0N1ozNVMwc3NnRm5FaDRxbG1nUUlEMyIsImlhdCI6MTY5OTM5NTMwOSwiZXhwIjoxNjk5Mzk4OTA5LCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImFub255bW91cyJ9fQ.RXR051YTxyIxvpcw_RAKDwR_CESJaSj8WP62LmArbiTAXYl5HoL_pApCYbQ8feYkOj2Ph27kc-ZtB1XOEVeYlWwm03TerkgRLdeMM-fWuJB2KJHCKcXeAcRR1_IsV2l5NdZMhnJLxX9yC-BRkpnV9cipWvIE98yD8idLu_hJtvtMq_u4ctRYf07go68lnqN4kuLpiygIV4mW3ZC4CeXKpvlTAU-fD9qcmlxZpa3jM-0_Bc8b5d07xmJjWRB25_P_r4-dlcxZjxBchL6y8rOu2mVQdLB5b2DF4-GLxO2G85GEG-87g-5MZrDlyxCuDQIakbB9KBSKkJK4rVVHSIDb6g',
            'drugstore-stock': '',
            'Content-Type': 'application/json',
            'Origin': 'https://www.mifarma.com.pe',
            'Connection': 'keep-alive',
            'Referer': 'https://www.mifarma.com.pe/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }      
        if headers:
            my_headers.update(headers)  
                                 
        my_payload = {  
        "departmentsFilter": [
            500141
        ],
        "categoriesFilter": [],
        "subcategoriesFilter": [],
        "brandsFilter": [],
        "ranking": None,
        "page": 0,
        "rows": 105,
        "order": "ASC",
        "sort": "ranking",
        "productsFilter": []
  }   
        if not my_payload:
           my_payload = data
        else:
            my_payload.update(data)     

        response = requests.request(method = method, url = url, headers=my_headers, data=my_payload)   
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la página {url} : {e}")
        return None    
    
