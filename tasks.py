import threading
import requests
from bs4 import BeautifulSoup
import random
import time

def get_random_user_agent():
    file_ua = "user-agent.txt"
    try:
        with open(file_ua, 'r') as file:
            lines = file.readlines()
            if lines:
                random_line = random.choice(lines)
                return random_line
            else:
                return "El archivo está vacío."
    except FileNotFoundError:
        return "El archivo no existe."

#linea = get_random_user_agent()
#print(linea)

def get_example():
    base_url = 'https://example.com'
    random_param = f'random={random.randint(1, 100000)}'  # Agrega un parámetro de consulta aleatorio
    url = f'{base_url}?{random_param}'
    response = requests.get(url)
    return response.text


"""
if __name__ == "__main__":
    inicio = time.time()  # Registro del tiempo de inicio
    for i in range(20):
        resultado = get_example()
        print(f'Resultado {i + 1:>2}: {len(resultado)} bytes')
    fin = time.time()  # Registro del tiempo de finalización

    tiempo_transcurrido = fin - inicio
    print(f'Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos')

"""

if __name__ == "__main__":
    num_hilos = 20  # Número de hilos que deseas ejecutar.
    inicio = time.time()

    hilos = []
    resultados = []

    for i in range(num_hilos):
        hilo = threading.Thread(target=lambda i=i: resultados.append((i, get_example())))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    fin = time.time()

    tiempo_transcurrido = fin - inicio

    for i, resultado in resultados:
        print(f'Resultado del hilo {i + 1}: {len(resultado)} bytes')

    print(f'Tiempo transcurrido: {tiempo_transcurrido:.2f} segundos')
