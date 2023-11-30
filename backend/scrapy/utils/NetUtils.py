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
    
    
    ##
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
        #print(f"Error al descargar la página: {e}")
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
    
  

def get_ip_public():
    data = download_json("https://ipwho.is/")
    ip_public = data["ip"]
    return ip_public 
    