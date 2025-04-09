# fastapi-csv_db

Documentación del Sistema de Gestión de Productos
Descripción General
Este sistema proporciona una API RESTful completa para gestionar productos almacenados en archivos CSV. La aplicación está construida con FastAPI y ofrece operaciones CRUD completas, incluyendo búsqueda avanzada.

Características Principales
✅ Operaciones CRUD completas para productos

✅ Búsqueda por nombre (coincidencia parcial)

✅ Validación de datos integrada

✅ Auto-generación de IDs

✅ Manejo de errores detallado

✅ Documentación automática con Swagger UI

Estructura del Proyecto
Copy
project/
├── database/
│   └── products.csv        # Archivo principal de datos
├── controllers/
│   └── products_controller.py  # Lógica de negocio
├── routes/
│   └── products_routes.py      # Definición de endpoints
├── utils/
│   └── csv_to_dict.py          # Utilidades para CSV
└── main.py                     # Punto de entrada
Instalación y Configuración
Requisitos previos:

Python 3.8+

Pipenv (recomendado)

Instalación:

bash
Copy
git clone [repo-url]
cd proyecto
pip install -r requirements.txt
Ejecución:

bash
Copy
uvicorn main:app --reload
Endpoints Disponibles
Productos
Método	Endpoint	Descripción
GET	/api/products/	Obtiene todos los productos
GET	/api/products/{id}	Obtiene un producto por ID
POST	/api/products/	Crea un nuevo producto
PUT	/api/products/{id}	Actualiza un producto existente
DELETE	/api/products/{id}	Elimina un producto
GET	/api/products/search/{query}	Busca productos por nombre
Ejemplos de Uso
Crear un producto
bash
Copy
curl -X POST "http://localhost:8000/api/products/" \
-H "Content-Type: application/json" \
-d '{
  "nombre": "Nuevo Producto",
  "descripcion": "Descripción de ejemplo",
  "precio": 99.99,
  "categoria": "Electrónica",
  "stock": 50,
  "marca": "MarcaEjemplo"
}'
Buscar productos
bash
Copy
curl "http://localhost:8000/api/products/search/portatil"
Documentación Interactiva
Accede a la documentación automática:

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

Estructura del CSV
El archivo CSV debe contener estas columnas:

id_producto (autogenerado)

nombre

descripcion

precio

categoria

stock

marca

fecha_creacion

Manejo de Errores
La API devuelve códigos de estado HTTP apropiados:

Código	Significado
200	OK - Operación exitosa
201	Created - Recurso creado
400	Bad Request - Datos inválidos
404	Not Found - Recurso no encontrado
500	Server Error - Error interno
Contribución
Haz fork del proyecto

Crea tu rama (git checkout -b feature/fooBar)

Haz commit de tus cambios (git commit -am 'Add some fooBar')

Haz push a la rama (git push origin feature/fooBar)

Crea un nuevo Pull Request
