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

## 💰 Funding

This resource is funded by the *Ministerio para la Transformación Digital y de la Función Pública* — Funded by **EU – NextGenerationEU**, within the framework of the project *Desarrollo de Modelos ALIA*.

## 🙏 Acknowledgments

We extend our gratitude to all individuals and institutions that contributed to the development of this resource.

Special thanks to:

- [Data providers]  
- [Technological support providers]

We also acknowledge the financial, scientific, and technical contributions of the *Ministerio para la Transformación Digital y de la Función Pública – Funded by EU – NextGenerationEU* within the framework of the *Desarrollo de Modelos ALIA* project.

## 📚 Reference

Please cite this dataset using the following BibTeX entry:

```bibtex
@misc{uji_parallel_va_en_2025,
  author       = {Espinosa Zaragoza, Sergio and Sep{\'u}lveda Torres, Robiert and Mu{\~n}oz Guillena, Rafael and Consuegra-Ayala, Juan Pablo}, <-- ACTUALIZAR
  title        = {ALIA_BOUA Scraper}, 
  year         = {2025},
  institution  = {Language and Information Systems Group (GPLSI) and Centro de Inteligencia Digital (CENID), University of Alicante (UA)},
  howpublished = {\url{https://huggingface.co/datasets/gplsi/uji_parallel_va_es}} <-- ACTUALIZAR
}
```

## ⚠️ Disclaimer

This resource may contain biases or unintended artifacts.
Any third party using or deploying systems based on this resource is solely responsible for ensuring compliant, safe, and ethical use, including adherence to relevant AI and data protection regulations.

The University of Alicante, as creator and owner of the resource, assumes no liability for outcomes resulting from third-party use.

## 📜 License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)


