# Configuración del Proyecto

Este documento detalla la configuración completa del proyecto, incluyendo las pruebas unitarias y la pipeline de CI/CD. Cada sección está diseñada para guiar al usuario a través del proceso de configuración y verificación del sistema.

## 1. Pruebas Unitarias

Las pruebas unitarias son fundamentales para garantizar la calidad y el correcto funcionamiento del microservicio. Esta sección explica la estructura de las pruebas, los casos de uso implementados y cómo ejecutarlas.

### Estructura de Pruebas
La estructura de pruebas está organizada de manera modular para facilitar el mantenimiento y la escalabilidad. Cada archivo tiene una responsabilidad específica:
- `conftest.py`: Contiene la configuración global y fixtures reutilizables
- `test_auth.py`: Pruebas relacionadas con la autenticación
- `test_blacklist.py`: Pruebas de los endpoints de la API
- `test_models.py`: Pruebas del modelo de datos
- `test_schemas.py`: Pruebas de validación de datos

### Casos de Uso Implementados

#### Autenticación
La autenticación es un componente crítico de seguridad. Las pruebas cubren:
- Verificación de token válido: Asegura que los tokens correctos sean aceptados
- Rechazo de token inválido: Garantiza que tokens incorrectos sean rechazados
- Manejo de solicitudes sin token: Verifica el comportamiento con solicitudes no autenticadas

#### Endpoints de Blacklist
Los endpoints son la interfaz principal del servicio. Las pruebas incluyen:
- Agregar correo a la lista negra:
  - Validación de formato: Asegura que solo se acepten correos válidos
  - Manejo de duplicados: Previene entradas repetidas
  - Validación de campos: Verifica que todos los campos requeridos estén presentes
- Verificar estado de correo:
  - Correo en lista negra: Confirma la detección de correos bloqueados
  - Correo no en lista negra: Verifica el manejo de correos permitidos
  - Manejo de inválidos: Asegura el correcto manejo de correos malformados
- Health Check:
  - Verificación de estado: Confirma que el servicio esté operativo

#### Modelos y Esquemas
Los modelos y esquemas son la base de datos del sistema. Las pruebas cubren:
- Validación de datos: Asegura la integridad de los datos
- Serialización/Deserialización: Verifica la correcta conversión de datos
- Relaciones entre modelos: Confirma las conexiones entre entidades

### Ejecución de Pruebas

#### Requisitos Previos
Antes de ejecutar las pruebas, es necesario instalar las dependencias de testing. Estas herramientas proporcionan:
- pytest: Framework de pruebas
- pytest-cov: Generación de reportes de cobertura
- pytest-flask: Integración con Flask

#### Comandos de Ejecución

1. Ejecutar todas las pruebas:
Este comando ejecuta todas las pruebas del sistema, proporcionando un resumen completo del estado del código.

2. Ejecutar pruebas con cobertura:
Genera un reporte detallado de cobertura de código, útil para identificar áreas que necesitan más pruebas.

3. Ejecutar pruebas específicas:
Permite ejecutar subconjuntos de pruebas para debugging o desarrollo específico.

### Capturas de Pantalla
Las capturas de pantalla documentan:
- La ejecución exitosa de pruebas
- El reporte de cobertura de código
Estas imágenes son evidencia del estado actual del sistema.

## 2. Configuración de AWS CodePipeline

La pipeline de CI/CD automatiza el proceso de construcción, prueba y despliegue del servicio. Esta sección detalla su configuración.

### Requisitos Previos
Antes de configurar la pipeline, se necesitan:
1. Una cuenta de AWS con los permisos adecuados para los servicios utilizados
2. AWS CLI configurado con credenciales válidas
3. Un repositorio de código en AWS CodeCommit para el control de versiones

### Paso a Paso de Configuración

#### 1. Creación del Repositorio ECR
El Elastic Container Registry (ECR) almacena las imágenes Docker del servicio:
1. Navegar a Amazon ECR en la consola de AWS
2. Crear un nuevo repositorio para las imágenes
3. Configurar las políticas de acceso según los requisitos de seguridad

#### 2. Configuración de CodeBuild
CodeBuild es el servicio que ejecuta el proceso de construcción:
1. Crear un nuevo proyecto de build en la consola de AWS
2. Configurar el origen del código (repositorio CodeCommit)
3. Seleccionar el entorno de build apropiado
4. Especificar el archivo buildspec.yml
5. Configurar las variables de entorno necesarias para el proceso

#### 3. Configuración de CodePipeline
CodePipeline orquesta todo el proceso de CI/CD:
1. Crear una nueva pipeline en la consola de AWS
2. Configurar la etapa de origen (CodeCommit)
3. Configurar la etapa de build (CodeBuild)
4. Opcionalmente, configurar la etapa de despliegue

### Archivo buildspec.yml
El archivo buildspec.yml define las etapas del proceso de construcción:
- install: Instala dependencias y herramientas
- pre_build: Ejecuta pruebas y prepara el entorno
- build: Construye la imagen Docker
- post_build: Sube la imagen a ECR

### Verificación de la Pipeline
Para asegurar que la pipeline funciona correctamente:
1. Ejecutar la pipeline manualmente desde la consola
2. Revisar los logs de build para identificar posibles problemas
3. Confirmar que la imagen se ha subido correctamente a ECR

### Solución de Problemas Comunes
Esta sección cubre los problemas más frecuentes:
1. Errores de permisos: Verificar IAM roles y políticas
2. Fallos en las pruebas: Revisar logs y corregir problemas en el código
3. Problemas de conectividad con ECR: Verificar configuración de red y credenciales 