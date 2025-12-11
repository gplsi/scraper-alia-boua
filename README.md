# 📄 Script de extracción del BOUA (Boletín Oficial de la Universidad de Alicante)

Este script automatiza la descarga y el procesamiento de acuerdos del BOUA (Boletín Oficial de la Universidad de Alicante). Recupera listados vía POST, abre cada acuerdo con Selenium, extrae metadatos y cuerpo con BeautifulSoup, guarda HTML y texto plano y genera un índice JSON con los registros (valenciano y castellano).

## 🧩 Resumen de funcionalidades

- Recupera listados paginados de acuerdos mediante petición POST a https://www.boua.ua.es/Acuerdos/buscarAcuerdos.

- Itera en un rango de páginas configurable, para cada página sacamos 20 boletines:

    - Carga la página del acuerdo con Selenium (en valenciano y en castellano).

    - Extrae título, fechas, órgano, sección y el cuerpo del acuerdo.

    - Guarda la página completa en HTML y el contenido en TXT.

    - Añade una entrada en un índice JSON con metadatos y rutas relativas a los ficheros.

- Genera un index.json con todas las entradas procesadas.

## 📁 Estructura de ficheros resultante
```
boua/
├── 2025/
│   ├── html/
│   │   ├── va/
│   │   │   └── acuerdo-<ID>.html
│   │   └── es/
│   │       └── acuerdo-<ID>.html
│   └── plain/
│       ├── va/
│       │   └── acuerdo-<ID>.txt
│       └── es/
│           └── acuerdo-<ID>.txt
└── index.json
```

## 🧰 Requisitos

### Dependencias (Python)

- `requests`

- `beautifulsoup4`

- `selenium`

- `json (stdlib)`

- `os (stdlib)`

Instalación recomendada:
```
pip install requests beautifulsoup4 selenium
```


### Requisitos del sistema

- Google Chrome instalado.

- ChromeDriver compatíble con la versión de Chrome.

- Entorno Windows / Linux / macOS.

- Espacio en disco suficiente para guardar HTML y TXT (depende del número de acuerdos).


## ▶️ Cómo ejecutar

1. Asegúrate de que las dependencias están instaladas y Chrome + ChromeDriver funcionan.

2. Crea las carpetas destino (o modifica el script para que las cree automáticamente):

```
mkdir -p boua/2025/html/va boua/2025/html/es boua/2025/plain/va boua/2025/plain/es
```

3. Ejecuta:

```
python boua.py
```

El script escribe el índice parcial/total en index.json tras cada página procesada.

### 🧭 Flujo de ejecución (detalle paso a paso)

**1. Bucle de páginas**

- Para cada `page`:

    - Construye `HEADERS` y envía `requests.post` a `https://www.boua.ua.es/Acuerdos/buscarAcuerdos` con el payload:
```
{
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
}
```

    - Si `response.status_code == 200`, parsea `response.json()`.

**2. Procesado de cada `acuerdo`**

- Para cada `acuerdo` en `data['acuerdos'][:20]`:

    - Imprime número de boletín.

    -   Crea una instancia nueva de ``webdriver.Chrome(options=options)`` (opciones: ``--headless``, ``--incognito``, ``--no-sandbox``, ``--ignore-certificate-errors``).

    - **Cargar versión valenciana**: driver.get('https://www.boua.ua.es/ca/acuerdo/<ID>')

        - ``bs = BeautifulSoup(driver.page_source, 'html.parser')``

        - Extrae:

            - ``title = bs.find('p', {'class': 'h1'})``

            - ``characteristics = bs.find_all('dd', {'class': 'col-sm-9'})``→ metadatos:

                - ``[0]`` → fecha de aprobación

                - ``[1]`` → fecha de publicación

                - ``[2]`` → órgano

                - ``[3]`` → sección

            - ``paragraphs = bs.find_all('div', {'class': 'parrafos_celda parrafos_celda_izq'})`` → contenido del boletín

        - Guarda:

            - HTML: ``boua/2025/html/va/acuerdo-<ID>.html``

            - TXT: ``boua/2025/plain/va/acuerdo-<ID>.txt``

        - Añade una entrada a un diccionario con campos ``source``, ``aprovation_date``, ``publication_date``, ``title``, ``section``, ``organ``, ``language``, ``path2html``, ``path2txt``.

    - **Cargar versión castellana**: mismo proceso con URL .../es/acuerdo/<ID>

**3. Guardar índice**

- Tras procesar cada página del boua con 20 boletines, escribe el diccionario en ``boua/index.json`` con ``json.dumps(..., ensure_ascii=False, indent=4)``.

## 🧾 Ejemplo de entrada/salida (registro JSON)

```
{
    "source": "https://www.boua.ua.es/va/acuerdo/12345",
    "aprovation_date": "01/02/2025",
    "publication_date": "05/02/2025",
    "title": "Aprobación de... ",
    "section": "Gestión",
    "organ": "Rectorado",
    "language": "va",
    "path2html": "/2025-02/html/va/acuerdo-12345.html",
    "path2txt": "/2025-02/plain/va/acuerdo-12345.txt"
}
```

## 💰 Financiación

Este recurso está financiado por el Ministerio para la Transformación Digital y de la Función Pública — Financiado por la UE – NextGenerationEU, en el marco del proyecto Desarrollo de Modelos ALIA.

## 🙏 Agradecimientos

Expresamos nuestro agradecimiento a todas las personas e instituciones que han contribuido al desarrollo de este recurso.

Agradecimientos especiales a:

[Proveedores de datos]

[Proveedores de soporte tecnológico]

Asimismo, reconocemos las contribuciones financieras, científicas y técnicas del Ministerio para la Transformación Digital y de la Función Pública – Financiado por la UE – NextGenerationEU dentro del marco del proyecto Desarrollo de Modelos ALIA.

## 📚 Referencia

Por favor, cita este conjunto de datos usando la siguiente entrada BibTeX:

@misc{uji_parallel_va_en_2025,
  author       = {Espinosa Zaragoza, Sergio and Sep{\'u}lveda Torres, Robiert and Mu{\~n}oz Guillena, Rafael and Consuegra-Ayala, Juan Pablo},
  title        = {ALIA_BOUA Scraper}, 
  year         = {2025},
  institution  = {Language and Information Systems Group (GPLSI) and Centro de Inteligencia Digital (CENID), University of Alicante (UA)},
  howpublished = {\url{https://huggingface.co/datasets/gplsi/uji_parallel_va_es}} <-- ACTUALIZAR
}

## ⚠️ Aviso Legal

Este recurso puede contener sesgos o artefactos no intencionados.
Cualquier tercero que utilice o implemente sistemas basados en este recurso es el único responsable de garantizar un uso conforme, seguro y ético, incluyendo el cumplimiento de las normativas relevantes en materia de IA y protección de datos.

La Universidad de Alicante, como creadora y propietaria del recurso, no asume ninguna responsabilidad por los resultados derivados del uso por parte de terceros.

## 📜 Licencia

Licencia Apache, Versión 2.0


