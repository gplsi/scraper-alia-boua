import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import json

if __name__ == '__main__':
    indexid = 3980
    news = []
    body = date_aprov = title = organ = section = date_pub = " "
    for page in range(299, 437):
        #Hacemos una llamada post para que nos devuelva 20 boletines del boua
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        response = requests.post('https://www.boua.ua.es/Acuerdos/buscarAcuerdos', data={
                "pag": page,
                "items_pag": 20,
                "texto": "",
                "fecha_apro_desde": "",
                "fecha_apro_hasta": "",
                "fecha_publ_desde": "",
                "fecha_publ_hasta": "",
                "organo": -1,
                "categoria": -1,
                "unipersonal": -1,
                "centro": -1,
                "publicados": True
        }, headers=HEADERS)
        if response.status_code == 200:
             data = response.json()
             #Partimos la respuesta para asegurarnos de que cojamos los primeros 20 y no repetir boletines
             for acuerdo in data['acuerdos'][:20]:
                 print("BOLETÍN NÚMERO:" + str(indexid))
                 options = webdriver.ChromeOptions()
                 options.add_argument('--ignore-certificate-errors')
                 options.add_argument('--incognito')
                 options.add_argument('--headless')
                 options.add_argument('--no-sandbox')
                 driver = webdriver.Chrome(options=options)
                 driver.get('https://www.boua.ua.es/ca/acuerdo/' + str(int(acuerdo['ID'])))
                 bs = BeautifulSoup(driver.page_source, 'html.parser')
                 #Extraemos la información
                 if bs:
                     path_html = "acuerdo-" + str(int(acuerdo['ID'])) + ".html"
                     path_txt = "acuerdo-" + str(int(acuerdo['ID'])) + ".txt"
                     characteristics = bs.find_all('dd', {'class': 'col-sm-9'})
                     title = bs.find('p', {'class': 'h1'})
                     if title:
                         title = title.text.strip()
                     if characteristics:
                         section = characteristics[3].text.strip()
                         organ = characteristics[2].text.strip()
                         date_aprov = characteristics[0].text.strip()
                         date_pub = characteristics[1].text.strip()
                     paragraphs = bs.find_all('div', {'class': 'parrafos_celda parrafos_celda_izq'})
                     body = " "
                     if paragraphs:
                         for paragraph in paragraphs:
                                 body += paragraph.text + '\n'
                         ruta = os.path.join("boua", "2025-02", "html", "va", path_html)
                         f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                         f.write(driver.page_source)
                         ruta = os.path.join("boua", "2025-02", "plain", "va", path_txt)
                         f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                         f.write(body)
                     news.append({'source': 'https://www.boua.ua.es/va/acuerdo/' + str(int(acuerdo['ID'])), 'aprovation_date': date_aprov, 'publication_date': date_pub, 'title': title,
                          'section': section, 'organ': organ, "language": "va", "path2html": "/2025-02/html/va/" + path_html, "path2txt": "/2025-02/plain/va/" + path_txt})
                 #Repetimos el proceso pero con el boletin en español
                 driver.get('https://www.boua.ua.es/es/acuerdo/' + str(int(acuerdo['ID'])))
                 bs = BeautifulSoup(driver.page_source, 'html.parser')
                 if bs:
                     path_html = "acuerdo-" + str(int(acuerdo['ID'])) + ".html"
                     path_txt = "acuerdo-" + str(int(acuerdo['ID'])) + ".txt"
                     characteristics = bs.find_all('dd', {'class': 'col-sm-9'})
                     title = bs.find('p', {'class': 'h1'})
                     if title:
                         title = title.text.strip()
                     if characteristics:
                         section = characteristics[3].text.strip()
                         organ = characteristics[2].text.strip()
                         date_aprov = characteristics[0].text.strip()
                         date_pub = characteristics[1].text.strip()
                     paragraphs = bs.find_all('div', {'class': 'parrafos_celda parrafos_celda_der'})
                     body = " "
                     if paragraphs:
                         for paragraph in paragraphs:
                             body += paragraph.text + '\n'
                         ruta = os.path.join("boua", "2025-02", "html", "es", path_html)
                         f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                         f.write(driver.page_source)
                         ruta = os.path.join("boua", "2025-02", "plain", "es", path_txt)
                         f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
                         f.write(body)
                     news.append(
                         {'source': 'https://www.boua.ua.es/es/acuerdo/' + str(int(acuerdo['ID'])), 'aprovation_date': date_aprov, 'publication_date': date_pub, 'title': title,
                          'section': section, 'organ': organ, "language": "es", "path2html": "/2025-02/html/es/" + path_html, "path2txt": "/2025-02/plain/es/" + path_txt})
                 indexid += 1
        print('PÁGINA NÚMERO: ' + str(page) + ' DE 436')
        ruta = os.path.join("boua", "index-3.json")
        f = open(os.getcwd() + "\\" + ruta, "w+", encoding='utf-8')
        f.write(json.dumps(news, indent=4, ensure_ascii=False))
