import time
import requests
import concurrent.futures
import signal


def get_wiki_page_existence(wiki_page_url, timeout=10):
    response = requests.get(url=wiki_page_url, timeout=timeout)

    page_status = "unknown"
    if response.status_code == 200:
        page_status = "exists"
    elif response.status_code == 404:
        page_status = "does not exist"

    return wiki_page_url + " - " + page_status

wiki_page_urls = ["https://en.wikipedia.org/wiki/" + str(i) for i in range(100)]

"""  
print("Running threaded:")
threaded_start = time.time()
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for url in wiki_page_urls:
        futures.append(executor.submit(get_wiki_page_existence, wiki_page_url=url))
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
    print("Threaded time:", time.time() - threaded_start)
    
"""
mi_lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ...]
mi_lista = mi_lista[:12]
primeros_10_elementos = mi_lista[:10]

print(primeros_10_elementos)


