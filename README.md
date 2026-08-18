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
