# Microservicio Blacklist

Este es un microservicio Flask que maneja una lista negra de correos electrónicos. Permite agregar correos a la lista negra y verificar si un correo está en la lista.

## Características

- API RESTful para gestionar la lista negra
- Autenticación mediante token JWT estático
- Validación de datos con Marshmallow
- Base de datos SQLite/PostgreSQL
- Endpoints:
  - POST `/blacklists/` - Agregar correo a la lista negra
  - GET `/blacklists/<email>` - Verificar si un correo está en la lista negra
  - GET `/blacklists/health` - Verificar estado del servicio

## Requisitos

- Python 3.7+
- pip
- PostgreSQL (opcional, para producción)

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd microservicio_blacklist
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Solución de Problemas

### Problemas de Dependencias

Si encuentras errores relacionados con dependencias (como `cannot import name 'url_quote' from 'werkzeug.urls'`), intenta los siguientes pasos:

1. Eliminar el entorno virtual actual:
```bash
deactivate
rm -rf venv
```

2. Crear un nuevo entorno virtual:
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

3. Reinstalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Si el problema persiste, intenta instalar las dependencias una por una:
```bash
pip install Flask==2.0.1
pip install Werkzeug==2.0.3
pip install SQLAlchemy==1.4.46
pip install Flask-SQLAlchemy==2.5.1
pip install Flask-Marshmallow==0.14.0
pip install marshmallow-sqlalchemy==0.29.0
pip install marshmallow==3.13.0
pip install psycopg2-binary==2.9.1
pip install python-dotenv==0.19.0
pip install gunicorn==20.1.0
pip install pytest==7.0.1
pip install pytest-flask==1.2.0
pip install pytest-cov==3.0.0
pip install black==22.1.0
pip install flake8==4.0.1
pip install isort==5.10.1
pip install mypy==0.910
```

### Problemas de Importación

Si encuentras errores como `No module named 'app'` al ejecutar los tests, asegúrate de ejecutar los tests desde el directorio raíz del proyecto y usa uno de los siguientes comandos:

```bash
# Opción 1: Usando PYTHONPATH
PYTHONPATH=$PYTHONPATH:. pytest tests/

# Opción 2: Usando el módulo pytest
python -m pytest tests/

# Opción 3: Usando el flag -p no:warnings para suprimir advertencias
python -m pytest tests/ -p no:warnings
```

### Problemas con SQLAlchemy

Si encuentras errores como `AttributeError: module 'sqlalchemy' has no attribute '__all__'`, esto indica un problema de compatibilidad entre las versiones de SQLAlchemy y Flask-SQLAlchemy. Para resolverlo:

1. Asegúrate de tener las versiones correctas instaladas:
```bash
pip uninstall sqlalchemy flask-sqlalchemy
pip install SQLAlchemy==1.4.46
pip install Flask-SQLAlchemy==2.5.1
```

2. Si el problema persiste, intenta limpiar la caché de pip:
```bash
pip cache purge
pip install -r requirements.txt
```

### Advertencias de Deprecación

Si ves advertencias como `DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead`, puedes manejarlas de las siguientes formas:

1. Actualizar a la última versión de marshmallow-sqlalchemy (ya incluida en requirements.txt):
```bash
pip install marshmallow-sqlalchemy==0.29.0
```

2. Suprimir las advertencias específicas al ejecutar los tests:
```bash
python -m pytest tests/ -p no:deprecation
```

3. Suprimir todas las advertencias:
```bash
python -m pytest tests/ -p no:warnings
```

4. Configurar Python para ignorar advertencias de deprecación:
```bash
export PYTHONWARNINGS="ignore::DeprecationWarning"
python -m pytest tests/
```

## Configuración

El servicio se puede configurar mediante variables de entorno o editando el archivo `config.py`:

- `FLASK_CONFIG`: Configuración a usar (DevelopmentConfig, TestingConfig, ProductionConfig)
- `SECRET_KEY`: Clave secreta para la aplicación
- `DATABASE_URL`: URL de conexión a la base de datos
- `JWT_STATIC_TOKEN`: Token JWT estático para autenticación

## Ejecución

### Desarrollo Local
```bash
python application.py
```

### Producción
```bash
gunicorn application:application
```

## Testing

El proyecto incluye una suite completa de pruebas unitarias y de integración.

### Ejecutar Tests
```bash
# Ejecutar todos los tests
python -m pytest tests/

# Ejecutar tests con cobertura
python -m pytest tests/ --cov=app

# Ejecutar tests con cobertura y reporte HTML
python -m pytest tests/ --cov=app --cov-report=html
```

### Estructura de Tests
- `tests/test_blacklist.py`: Tests para los endpoints de la API
- `tests/test_models.py`: Tests para el modelo Blacklist
- `tests/test_schemas.py`: Tests para la validación de datos
- `tests/test_auth.py`: Tests para la autenticación
- `tests/conftest.py`: Configuración y fixtures de pytest

## Desarrollo

### Formateo de Código
```bash
# Formatear código con black
black .

# Verificar estilo con flake8
flake8

# Ordenar imports
isort .
```

### Verificación de Tipos
```bash
mypy .
```

## Estructura del Proyecto

```
microservicio_blacklist/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── prod.db
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_blacklist.py
│   ├── test_models.py
│   └── test_schemas.py
├── .ebextensions/
├── application.py
├── config.py
├── Procfile
├── README.md
└── requirements.txt
```

## API Documentation

### Agregar a Lista Negra
```http
POST /blacklists/
Authorization: Bearer <token>
Content-Type: application/json

{
    "email": "test@example.com",
    "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "reason": "Test reason"
}
```

### Verificar Lista Negra
```http
GET /blacklists/test@example.com
Authorization: Bearer <token>
```

### Health Check
```http
GET /blacklists/health
```

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
