# Microservicio Blacklist

## Tabla de Contenidos
1. [Características](#características)
2. [Requisitos](#requisitos)
3. [Instalación](#instalación)
4. [Configuración](#configuración)
5. [Ejecución](#ejecución)
   - [Desarrollo Local](#desarrollo-local)
   - [Producción](#producción)
6. [Docker](#docker)
7. [Testing](#testing)
   - [Configuración del Entorno de Testing](#configuración-del-entorno-de-testing)
   - [Ejecutar Tests](#ejecutar-tests)
   - [Estructura de Tests](#estructura-de-tests)
   - [Fixtures Disponibles](#fixtures-disponibles)
8. [Desarrollo](#desarrollo)
   - [Formateo de Código](#formateo-de-código)
   - [Verificación de Tipos](#verificación-de-tipos)
9. [Estructura del Proyecto](#estructura-del-proyecto)
10. [API Documentation](#api-documentation)
11. [Contribución](#contribución)
12. [Licencia](#licencia)

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

4. Configurar variables de entorno:
```bash
# Crear archivo .env
cp .env.example .env
# Editar .env con tus configuraciones
```

## Configuración

El servicio se puede configurar mediante variables de entorno en el archivo `.env`:

```env
# Environment Configuration
FLASK_CONFIG=config.DevelopmentConfig

# Application Settings
SECRET_KEY=your_secret_key
JWT_STATIC_TOKEN=your_jwt_token

# Database Configuration
DATABASE_URL=sqlite:///dev.db  # Para desarrollo
# DATABASE_URL=postgresql://user:password@localhost:5432/blacklist_db  # Para producción
```

## Ejecución

### Desarrollo Local
```bash
# Activar entorno virtual si no está activo
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Ejecutar aplicación
python application.py
```

### Producción
```bash
gunicorn application:application
```

## Docker

El servicio puede ser ejecutado usando Docker para un despliegue más sencillo y consistente.

### Construir la Imagen
```bash
docker build -t blacklist-microservice .
```

### Ejecutar el Contenedor
```bash
docker run -p 5000:5000 blacklist-microservice
```

### Variables de Entorno
Puedes configurar el servicio usando variables de entorno al ejecutar el contenedor:

```bash
docker run -p 5000:5000 \
  -e FLASK_CONFIG=config.ProductionConfig \
  -e SECRET_KEY=your_secret_key \
  -e JWT_STATIC_TOKEN=your_jwt_token \
  -e DATABASE_URL=postgresql://user:password@host:5432/dbname \
  blacklist-microservice
```

### Docker Compose
Para un despliegue más completo que incluya la base de datos PostgreSQL, puedes usar Docker Compose:

```bash
# Construir y ejecutar los servicios
docker-compose up -d

# Detener los servicios
docker-compose down
```

## CI/CD Pipeline

El proyecto incluye una pipeline de CI/CD configurada con AWS CodeBuild. La pipeline ejecuta las siguientes etapas:

### Etapas de la Pipeline

1. **Instalación**
   - Configura Python 3.9 como versión de runtime
   - Instala dependencias del proyecto
   - Instala herramientas de testing y calidad de código

2. **Pre-Build**
   - Ejecuta verificaciones de calidad de código:
     - Black (formateo de código)
     - Flake8 (linting)
     - Isort (ordenamiento de imports)
     - Mypy (verificación de tipos)
   - Ejecuta tests unitarios con cobertura
   - Inicia sesión en Amazon ECR

3. **Build**
   - Construye la imagen Docker
   - Etiqueta la imagen con el repositorio ECR

4. **Post-Build**
   - Sube la imagen Docker a ECR

### Reportes y Artefactos

La pipeline genera y almacena:
- Reportes de cobertura de código (formato Cobertura)
- Reportes de tests (formato JUnit XML)
- Artefactos de build

### Configuración

La pipeline está configurada en el archivo `buildspec.yml` en la raíz del proyecto. Para ejecutar la pipeline localmente:

```bash
# Instalar CodeBuild CLI
pip install aws-sam-cli

# Ejecutar build local
aws codebuild start-build --project-name <nombre-del-proyecto>
```

### Requisitos de la Pipeline

Para que la pipeline se ejecute correctamente, asegúrate de:
1. Tener configuradas las variables de entorno necesarias en AWS CodeBuild:
   - `AWS_DEFAULT_REGION`
   - `AWS_ACCOUNT_ID`
   - `IMAGE_REPO_NAME`
   - `IMAGE_TAG`
2. Tener los permisos necesarios para acceder a ECR
3. Mantener una cobertura de tests adecuada (recomendado >80%)

## Testing

El proyecto incluye una suite completa de pruebas unitarias y de integración.

### Configuración del Entorno de Testing

1. Asegúrate de que el entorno virtual esté activo
2. Verifica que las dependencias de testing estén instaladas:
```bash
pip install pytest pytest-flask pytest-cov
```

### Ejecutar Tests

#### Ejecutar Todos los Tests
```bash
# Desde el directorio raíz del proyecto
python -m pytest tests/
```

#### Ejecutar Tests con Cobertura
```bash
# Cobertura básica
python -m pytest tests/ --cov=app

# Cobertura con reporte HTML
python -m pytest tests/ --cov=app --cov-report=html

# Cobertura con reporte detallado
python -m pytest tests/ --cov=app --cov-report=term-missing
```

#### Ejecutar Tests Específicos
```bash
# Ejecutar un archivo específico
python -m pytest tests/test_blacklist.py

# Ejecutar una clase específica
python -m pytest tests/test_blacklist.py::TestBlacklistEndpoints

# Ejecutar un test específico
python -m pytest tests/test_blacklist.py::TestBlacklistEndpoints::test_add_to_blacklist
```

#### Opciones Adicionales
```bash
# Ejecutar tests con verbosidad aumentada
python -m pytest tests/ -v

# Ejecutar tests y mostrar prints
python -m pytest tests/ -s

# Ejecutar tests y detenerse al primer fallo
python -m pytest tests/ -x

# Ejecutar tests y mostrar tiempos de ejecución
python -m pytest tests/ --durations=3
```

### Estructura de Tests

```
tests/
├── conftest.py           # Configuración global y fixtures
├── test_auth.py          # Tests de autenticación
├── test_blacklist.py     # Tests de endpoints de la API
├── test_models.py        # Tests del modelo Blacklist
└── test_schemas.py       # Tests de validación de datos
```

### Fixtures Disponibles

- `app`: Instancia de la aplicación Flask configurada para testing
- `client`: Cliente de prueba para hacer requests a la API
- `runner`: CliRunner para probar comandos de CLI
- `valid_token`: Token JWT válido para testing
- `invalid_token`: Token JWT inválido para testing
- `sample_blacklist_entry`: Datos de ejemplo para testing

### Ejemplo de Uso de Fixtures

```python
def test_example(client, valid_token, sample_blacklist_entry):
    response = client.post(
        "/blacklists/",
        json=sample_blacklist_entry,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 201
```

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
