# DJANGOP2C1---LGODOY
# EcoEnergy - Back End

## Descripción

EcoEnergy es un proyecto Back End desarrollado con **Python** y **Django**. Este repositorio contiene la lógica del servidor, la estructura del proyecto y los componentes necesarios para el desarrollo de la aplicación.

## Objetivo

El objetivo de este proyecto es construir una base sólida para el desarrollo del Back End, siguiendo buenas prácticas de organización, mantenimiento y escalabilidad.

> **Nota:** Este documento corresponde a la configuración inicial del proyecto y se actualizará a medida que avance el desarrollo.

---

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

* Python
* Git
* pip (administrador de paquetes de Python)

---

## Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd EcoEnergy
```

> Reemplaza `<URL_DEL_REPOSITORIO>` por la dirección correspondiente cuando el repositorio esté disponible.

---

## Crear y activar el entorno virtual

### Crear el entorno virtual

```bash
python -m venv .venv
```

### Activar el entorno virtual

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD)**

```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

---

## Instalar las dependencias

Con el entorno virtual activado, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

## Comandos de verificación

Verificar que Django esté correctamente instalado:

```bash
python -m django --version
```

Verificar la configuración del proyecto:

```bash
python manage.py check
```

Aplicar las migraciones existentes (si corresponde):

```bash
python manage.py migrate
```

Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

Si todo está configurado correctamente, el servidor iniciará sin errores.

---

## Estado actual

* Proyecto Back End inicializado.
* Estructura base del proyecto en desarrollo.
* Configuración del entorno mediante entorno virtual.
* Gestión de dependencias mediante `requirements.txt`.

---

## Próximos pasos

* Definir la estructura de la aplicación.
* Implementar los modelos de datos.
* Configurar la base de datos según las necesidades del proyecto.
* Desarrollar la lógica de negocio.
* Implementar los endpoints de la API.
* Incorporar pruebas y documentación técnica.
* Actualizar este README conforme evolucione el proyecto.

---

## Estructura del proyecto

```text
Proyecto Integrado/
└── EcoEnergy/
    ├── .venv/
    ├── requirements.txt
    ├── manage.py
    └── ...
```

> La estructura podrá modificarse a medida que avance el desarrollo del proyecto.



# EcoEnergy

Aplicación web desarrollada con **Python y Django** para la consulta de zonas de consumo energético y los dispositivos instalados en ellas.

La aplicación utiliza archivos **JSON como fuente de datos** y procesa dinámicamente las relaciones entre zonas, categorías y dispositivos para mostrar la información mediante Templates y Bootstrap.

## Requisitos

Para ejecutar el proyecto se requiere:

* Python 3.x
* pip
* Git
* Django
* Navegador web

Las dependencias utilizadas por el proyecto se encuentran en:

```text
requirements.txt
```

Los archivos de datos requeridos son:

```text
zonas.json
categorias.json
dispositivos.json
```

### Datos mínimos requeridos

* `zonas.json`: mínimo 3 registros.
* `categorias.json`: mínimo 3 registros.
* `dispositivos.json`: mínimo 8 registros.

Los identificadores deben ser únicos y las relaciones mediante `zona_id` y `categoria_id` deben corresponder a registros existentes.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

Ingresar a la carpeta del proyecto:

```bash
cd EcoEnergy
```

### 2. Crear el entorno virtual

En Windows:

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

En Windows:

```bash
.venv\Scripts\activate
```

En Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución

Con el entorno virtual activado, ejecutar:

```bash
python manage.py runserver
```

Luego acceder desde el navegador a:

```text
http://127.0.0.1:8000/
```

Para comprobar la configuración del proyecto:

```bash
python manage.py check
```

El resultado esperado es:

```text
System check identified no issues
```

---

## Rutas funcionales

La aplicación cuenta con las siguientes rutas principales:

| Ruta                        | Descripción                                        |
| --------------------------- | -------------------------------------------------- |
| `/`                         | Página de inicio                                   |
| `/zonas/`                   | Lista todas las zonas registradas                  |
| `/zonas/<id>/`              | Muestra el detalle de una zona                     |
| `/zonas/<id>/dispositivos/` | Muestra los dispositivos pertenecientes a una zona |

### Listado de zonas

```text
http://127.0.0.1:8000/zonas/
```

Esta ruta debe mostrar todas las zonas registradas en `zonas.json`, indicando su nombre, límite de consumo, cantidad de dispositivos y acceso al detalle.

### Detalle de una zona

```text
http://127.0.0.1:8000/zonas/1/
```

Muestra la información de la zona seleccionada, incluyendo dispositivos, categoría, consumo total y estado.

El estado de la zona se determina mediante:

```text
NORMAL → consumo_total <= limite_kwh
ALERTA → consumo_total > limite_kwh
```

### Dispositivos de una zona

```text
http://127.0.0.1:8000/zonas/1/dispositivos/
```

Muestra los dispositivos asociados a la zona indicada.

---

## Pruebas

Las pruebas deben comprobar que la aplicación procese los datos de forma dinámica y continúe funcionando cuando cambie la información de los archivos JSON.

### 1. Verificación del proyecto

Ejecutar:

```bash
python manage.py check
```

**Resultado esperado:** el proyecto no presenta errores de configuración.

### 2. Agregar nuevos dispositivos

Agregar dos dispositivos válidos a `dispositivos.json`.

**Resultado esperado:**

* Los nuevos dispositivos aparecen automáticamente.
* Se actualiza la cantidad de dispositivos.
* Se actualiza el consumo total.
* Se actualiza el estado cuando corresponde.

No debe ser necesario modificar manualmente las Views o Templates para cada nuevo registro.

### 3. Aumentar la cantidad de datos

Duplicar temporalmente varios registros válidos en los archivos JSON.

**Resultado esperado:**

La interfaz mantiene su estructura, navegación y acceso al contenido.

### 4. Zona sin dispositivos

Dejar una zona sin dispositivos asociados.

**Resultado esperado:**

La aplicación continúa funcionando y muestra un mensaje comprensible, por ejemplo:

```text
Esta zona no tiene dispositivos.
```

### 5. Identificador inexistente

Solicitar una zona que no existe, por ejemplo:

```text
http://127.0.0.1:8000/zonas/999/
```

**Resultado esperado:**

La aplicación responde con un **404 controlado**, sin mostrar una falla técnica al usuario.

### 6. Estados NORMAL y ALERTA

Utilizar datos que permitan comprobar ambos estados.

**Resultado esperado:**

```text
NORMAL → consumo_total <= limite_kwh
ALERTA → consumo_total > limite_kwh
```

Los estados deben mostrarse mediante texto y apoyo visual, no solamente mediante colores.

### 7. Tablas con muchos registros

Aumentar temporalmente la cantidad de dispositivos.

**Resultado esperado:**

Las tablas permiten desplazamiento dentro de su contenedor y la página no presenta desbordamiento general ni pierde acceso a la navegación o controles.

---

## Comportamiento dinámico

La aplicación debe trabajar directamente con los datos contenidos en los archivos JSON.

Al agregar registros válidos, las cantidades, sumas, relaciones y estados deben actualizarse automáticamente sin modificar el código para cada elemento agregado.

La solución también debe mantenerse operativa cuando una zona no tenga dispositivos registrados.

---

## Tecnologías utilizadas

* Python
* Django
* HTML
* CSS
* Bootstrap
* JSON

---

## Estructura de datos

Los archivos utilizados por la aplicación son:

### zonas.json

Contiene:

```text
id
nombre
limite_kwh
```

### categorias.json

Contiene:

```text
id
nombre
descripcion
```

### dispositivos.json

Contiene:

```text
id
nombre
consumo_kwh
zona_id
categoria_id
```

---

## Alcance de la Fase 1

Esta versión se centra en la carga, procesamiento y presentación de datos mediante Django.

No forman parte del alcance de esta fase:

* Models
* Migraciones
* ORM
* CRUD
* Formularios
* Autenticación
* Permisos
* Soft delete
* Múltiples organizaciones
