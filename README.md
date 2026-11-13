# Taller 3: APIs Públicas, MongoDB y EDA

Curso: **Bases de Datos para Ciencia de Datos** · Docente: Miguel Ramos García
Autor: Manuel Araujo Cardenas Colmenares ·

## Descripción
Flujo de Ciencia de Datos de extremo a extremo:

1. **Extracción:** se consumen cervecerías desde la API pública [Open Brewery DB](https://openbrewerydb.org), que no requiere llave. Se descargan 400 registros (el mínimo exigido es 100).
2. **Almacenamiento RAW:** `ingesta.py` guarda el JSON sin modificar en MongoDB (base `taller3_db`, colección `raw_data`), usando el `id` de la API como `_id`. Se usa *upsert*, así que ejecutar el script varias veces no duplica documentos.
3. **Procesamiento y EDA:** `analisis.ipynb` lee la colección, crea un DataFrame con 10 variables, lo limpia, calcula 5 insights y genera 3 gráficos (1 torta y 2 libres).

## API utilizada
- Endpoint: `https://api.openbrewerydb.org/v1/breweries?per_page=200&page=N`
- Campos relevantes: `id`, `name`, `brewery_type`, `city`, `state_province`, `country`, `latitude`, `longitude`, `website_url`, `phone`, `postal_code`.

## Estructura del repositorio
```
├── README.md
├── requirements.txt
├── ingesta.py        # extracción (API) y carga (MongoDB)
├── analisis.ipynb    # selección de variables, EDA y gráficos
└── .gitignore
```

## Cómo ejecutarlo
**Prerrequisitos:** Python 3.10 o superior y una base de datos MongoDB (local con Community Server, o en la nube con MongoDB Atlas).

```bash
# 1. Clonar el repositorio e ingresar a la carpeta
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_repositorio>

# 2. Crear el entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate          # Windows (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt

# 3. Configurar la conexión a MongoDB
#    Crear un archivo .env en la raíz con una sola línea:
#    MONGO_URI=mongodb+srv://USUARIO:CLAVE@cluster0.xxxxx.mongodb.net/
#    (si se omite, se usa mongodb://localhost:27017)

# 4. Ingesta: API -> MongoDB
python ingesta.py

# 5. Análisis: abrir y ejecutar todas las celdas
jupyter notebook analisis.ipynb
```

El archivo `.env` contiene credenciales y está excluido del repositorio mediante `.gitignore`.

Para verificar la ingesta, la colección `taller3_db.raw_data` debe contener 400 documentos.

## Variables analizadas (10)
`name`, `brewery_type`, `city`, `state_province`, `country`, `latitude`, `longitude`, `website_url`, `phone`, `postal_code`.

## Insights calculados
1. Tipo de cervecería más frecuente y su porcentaje.
2. Estado o provincia con más cervecerías.
3. Ciudad con más cervecerías.
4. Porcentaje de cervecerías con sitio web.
5. Número de países en la muestra y país dominante.

## Visualizaciones
1. Gráfico de torta: proporción de cervecerías por tipo.
2. Gráfico de barras: Top 10 de estados o provincias.
3. Histograma: distribución de la latitud.