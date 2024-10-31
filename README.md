# GraFiles

**GraFiles** es un sistema de gestión de archivos en la nube desarrollado utilizando Flask, MongoDB y Docker. Permite a los usuarios almacenar, compartir y gestionar archivos de manera sencilla y eficiente.

## Características

- Registro e inicio de sesión de usuarios.
- Gestión de archivos (subida, eliminación, visualización).
- Compartición de archivos entre usuarios.
- Organización de archivos en carpetas.
- Funcionalidad de papelera para la recuperación de archivos eliminados.

## Tecnologías Utilizadas

- **Backend**: Flask
- **Base de Datos**: MongoDB
- **Contenerización**: Docker
- **Servidor Web**: Nginx
- **Lenguajes**: Python, HTML, CSS, JavaScript

## Requisitos

- [Docker](https://www.docker.com/get-started) (incluye Docker Compose)
- [MongoDB](https://www.mongodb.com/try/download/community) (opcional, ya que se usa Docker)
- Python 3.12 (si se quiere correr localmente sin Docker)

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://https://github.com/MunguiaMander/GraFiles
   cd grafiles

2. **Configura el entonrno**

    Si decides correr el proyecto sin Docker, crea un entorno virtual y activa:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    .\venv\Scripts\activate  # En Windows
3. **Instala las dependencias:**

    Asegúrate de estar en el directorio `app/backend` y ejecuta:
    ```bash
    pip install -r requirements.txt
4. **Ejecuta MongoDB**
    Si no estás usando Docker, asegúrate de tener MongoDB en funcionamiento en tu máquina.
5. **Ejecuta el Proyecto**
    ```bash
    docker-compose up --build
    python main.py

# Uso
Accede a la aplicación a través de tu navegador en `http://localhost:9000.`

## Rutas Principales
`/login`: Página de inicio de sesión.
`/register`: Página de registro.
`/dashboard`: Página principal de gestión de archivos.

# Estructura del Proyecto
            Grafiles:.
            │   docker-compose.yaml
            │   README.md
            │   requirements.txt
            │
            ├───app
            │   ├───backend
            │   │   │   app.py
            │   │   │   config.py
            │   │   │   main.py
            │   │   │   requirements.txt
            │   │   │
            │   │   ├───app
            │   │   │   └───frontend
            │   │   │       └───static
            │   │   │           └───uploads
            │   │   │                   imegen1.png
            │   │   │
            │   │   ├───models
            │   │   │   │   file_model.py
            │   │   │   │   user_model.py
            │   │   │   │
            │   │   │   └───__pycache__
            │   │   │           file_model.cpython-312.pyc
            │   │   │           file_model.cpython-39.pyc
            │   │   │           user_model.cpython-312.pyc
            │   │   │           user_model.cpython-39.pyc
            │   │   │
            │   │   ├───routes
            │   │   │   │   auth.py
            │   │   │   │   dashboard.py
            │   │   │   │   file_routes.py
            │   │   │   │   test_routes.py
            │   │   │   │   user_routes.py
            │   │   │   │
            │   │   │   └───__pycache__
            │   │   │           auth.cpython-312.pyc
            │   │   │           auth.cpython-39.pyc
            │   │   │           dashboard.cpython-312.pyc
            │   │   │           dashboard.cpython-39.pyc
            │   │   │           file_routes.cpython-312.pyc
            │   │   │           file_routes.cpython-39.pyc
            │   │   │           test_routes.cpython-312.pyc
            │   │   │           test_routes.cpython-39.pyc
            │   │   │           user_routes.cpython-312.pyc
            │   │   │           user_routes.cpython-39.pyc
            │   │   │
            │   │   ├───services
            │   │   │   │   file_service.py
            │   │   │   │   user_service.py
            │   │   │   │
            │   │   │   └───__pycache__
            │   │   │           file_service.cpython-312.pyc
            │   │   │           file_service.cpython-39.pyc
            │   │   │           user_service.cpython-312.pyc
            │   │   │           user_service.cpython-39.pyc
            │   │   │
            │   │   ├───utils
            │   │   │   │   auth_middleware.py
            │   │   │   │
            │   │   │   └───__pycache__
            │   │   │           auth_middleware.cpython-312.pyc
            │   │   │           auth_middleware.cpython-39.pyc
            │   │   │
            │   │   └───__pycache__
            │   │           app.cpython-312.pyc
            │   │           config.cpython-312.pyc
            │   │           config.cpython-39.pyc
            │   │           main.cpython-312.pyc
            │   │
            │   └───frontend
            │       │   nginx.conf
            │       │
            │       ├───static
            │       │   ├───css
            │       │   │       styles.css
            │       │   │
            │       │   ├───img
            │       │   │       txt_icon.jpg
            │       │   │       txt_icon.png
            │       │   │
            │       │   ├───js
            │       │   │       dashboard.js
            │       │   │       register.js
            │       │   │       scripts.js
            │       │   │       shared.js
            │       │   │
            │       │   └───uploads
            │       │           eventoejemplouno.png
            │       │           imegen1.png
            │       │
            │       └───templates
            │               dashboard.html
            │               login.html
            │               register.html
            │               shared.html
            │
            ├───docs
            └───script
                    db_script.js

# Inicializacion 
Puedes inicializar las colecciones en MongoDB ejecutando el siguiente script:

    mongosh
    use grafiles_db;

    db.createCollection("users");
    db.createCollection("files");
    db.createCollection("shared");
    db.createCollection("thrashed");