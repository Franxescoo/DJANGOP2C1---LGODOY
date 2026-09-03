# Análisis EcoEnergy

## 1. Descripción del modelo

La aplicación EcoEnergy trabaja con tres colecciones de datos almacenadas en archivos JSON:

* `zonas.json`
* `categorias.json`
* `dispositivos.json`

Estas colecciones representan las zonas de consumo energético, las categorías de los dispositivos y los dispositivos instalados en cada zona.

La información se carga desde los archivos JSON y las relaciones entre los registros se resuelven mediante estructuras y operaciones de Python.

---

## 2. Entidades y atributos

### Zona

Archivo:

```text
zonas.json
```

Atributos:

| Atributo     | Descripción                        |
| ------------ | ---------------------------------- |
| `id`         | Identificador único de la zona     |
| `nombre`     | Nombre de la zona                  |
| `limite_kwh` | Límite máximo de consumo permitido |

### Categoría

Archivo:

```text
categorias.json
```

Atributos:

| Atributo      | Descripción                         |
| ------------- | ----------------------------------- |
| `id`          | Identificador único de la categoría |
| `nombre`      | Nombre de la categoría              |
| `descripcion` | Descripción de la categoría         |

### Dispositivo

Archivo:

```text
dispositivos.json
```

Atributos:

| Atributo       | Descripción                                   |
| -------------- | --------------------------------------------- |
| `id`           | Identificador único del dispositivo           |
| `nombre`       | Nombre del dispositivo                        |
| `consumo_kwh`  | Consumo energético del dispositivo            |
| `zona_id`      | Identificador de la zona a la que pertenece   |
| `categoria_id` | Identificador de la categoría del dispositivo |

---

## 3. Relaciones

### Zona - Dispositivo

Una zona puede tener **cero o muchos dispositivos**.

Un dispositivo pertenece a **una zona**.

La relación se establece mediante:

```text
dispositivos.zona_id → zonas.id
```

Multiplicidad:

```text
Zona 1 ───────── 0..* Dispositivos
```

Esto permite que una zona no tenga dispositivos sin provocar que la aplicación deje de funcionar.

---

### Categoría - Dispositivo

Una categoría puede estar asociada a **cero o muchos dispositivos**.

Un dispositivo pertenece a **una categoría**.

La relación se establece mediante:

```text
dispositivos.categoria_id → categorias.id
```

Multiplicidad:

```text
Categoría 1 ───────── 0..* Dispositivos
```

---

## 4. Claves de conexión

Las claves utilizadas para resolver las relaciones son:

```text
zonas.id
    ↑
    │
dispositivos.zona_id
```

y:

```text
categorias.id
    ↑
    │
dispositivos.categoria_id
```

Por lo tanto, cada `zona_id` y `categoria_id` presente en `dispositivos.json` debe corresponder a un registro existente en su respectivo archivo.

Los identificadores deben ser únicos dentro de cada archivo.

---

## 5. Procesamiento de los datos

La aplicación carga los tres archivos JSON y procesa sus relaciones mediante Python.

Para obtener los datos de una zona se realiza conceptualmente el siguiente proceso:

```text
1. Buscar la zona mediante su ID.
2. Buscar los dispositivos cuyo zona_id corresponde al ID de la zona.
3. Obtener la categoría de cada dispositivo mediante categoria_id.
4. Calcular el consumo total de la zona.
5. Comparar el consumo total con limite_kwh.
6. Determinar el estado de la zona.
7. Enviar la información al Template.
```

### Cálculo del consumo total

El consumo total corresponde a la suma de los valores:

```text
consumo_total = suma(consumo_kwh de los dispositivos de la zona)
```

### Determinación del estado

La regla utilizada es:

```text
Si consumo_total > limite_kwh
    Estado = ALERTA

Si consumo_total <= limite_kwh
    Estado = NORMAL
```

Esto permite que el estado se actualice automáticamente cuando cambien los datos de los archivos JSON.

---

## 6. Manejo de casos especiales

### Zona sin dispositivos

Una zona puede existir sin dispositivos asociados.

En este caso:

* La aplicación continúa funcionando.
* El consumo total corresponde a cero o al valor calculado según los registros existentes.
* Se muestra un mensaje indicando que la zona no tiene dispositivos.

Mensaje esperado:

```text
Esta zona no tiene dispositivos.
```

### Zona inexistente

Cuando se solicita un identificador de zona que no existe:

```text
/zonas/<id>/
```

la aplicación debe responder mediante un **404 controlado**.

Esto evita mostrar errores técnicos al usuario.

---

## 7. Criterios de aceptación y pruebas

| Criterio                                                                                          | Archivo/Componente                                                           | Prueba                                                                                         |
| ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| CA-01. El listado muestra todas las zonas registradas.                                            | `zonas.json`, View de zonas, Template de listado                             | Abrir `/zonas/` y comprobar que aparecen todas las zonas del JSON.                             |
| CA-02. Cada zona muestra nombre, límite, cantidad de dispositivos y acceso al detalle.            | View de zonas, Template de zonas                                             | Revisar cada tarjeta o elemento del listado.                                                   |
| CA-03. El detalle muestra dispositivos, categoría, consumo, métricas y estado.                    | View de detalle, `dispositivos.json`, `categorias.json`, Template de detalle | Abrir `/zonas/<id>/` y verificar la información mostrada.                                      |
| CA-04. Las cantidades, sumas y estados se calculan dinámicamente.                                 | Views, procesamiento Python                                                  | Modificar los registros JSON y comprobar que cambian los resultados sin modificar el Template. |
| CA-05. ALERTA cuando `consumo_total > limite_kwh` y NORMAL cuando `consumo_total <= limite_kwh`.  | View de detalle, lógica de cálculo, Template                                 | Utilizar datos que produzcan ambos estados y comprobar el resultado.                           |
| CA-06. Los nuevos registros válidos se incorporan sin modificar una View o Template por elemento. | Archivos JSON, Views, Templates                                              | Agregar nuevos dispositivos y comprobar que aparecen automáticamente.                          |
| CA-07. Una zona sin dispositivos mantiene la aplicación operativa.                                | View de detalle, Template                                                    | Dejar una zona sin dispositivos y comprobar que aparece el mensaje correspondiente.            |
| CA-08. Un identificador inexistente responde mediante 404 controlado.                             | View de detalle, URLs                                                        | Solicitar `/zonas/999/` y comprobar la respuesta 404.                                          |
| CA-09. La interfaz conserva su estructura al aumentar los datos.                                  | Templates, Bootstrap, CSS                                                    | Aumentar la cantidad de zonas y dispositivos y revisar la navegación.                          |
| CA-10. Las tablas extensas permiten desplazamiento.                                               | Template, Bootstrap/CSS                                                      | Aumentar los registros y comprobar que la tabla se desplaza sin desbordar la página.           |
| CA-11. Existe jerarquía visual coherente.                                                         | Templates, Bootstrap                                                         | Revisar header, navegación, títulos, tablas, tarjetas, botones y mensajes.                     |
| CA-12. Los estados utilizan texto y apoyo visual.                                                 | Templates                                                                    | Verificar que NORMAL y ALERTA aparecen como texto además del uso de color.                     |
| CA-13. El proyecto se instala y supera `python manage.py check`.                                  | Proyecto Django, `requirements.txt`                                          | Instalar dependencias y ejecutar `python manage.py check`.                                     |

---

## 8. Pruebas mínimas realizadas

### Prueba 1: Nuevos registros

**Acción:** agregar dos dispositivos válidos a `dispositivos.json`.

**Resultado esperado:** los dispositivos aparecen automáticamente y se actualizan las cantidades, el consumo y el estado correspondiente.

### Prueba 2: Mayor volumen de datos

**Acción:** aumentar temporalmente la cantidad de registros válidos.

**Resultado esperado:** la estructura de la interfaz, navegación y controles permanecen utilizables.

### Prueba 3: Zona sin dispositivos

**Acción:** eliminar temporalmente la relación de dispositivos de una zona.

**Resultado esperado:** la aplicación sigue funcionando y muestra un mensaje indicando la ausencia de dispositivos.

### Prueba 4: Identificador inexistente

**Acción:** acceder a:

```text
/zonas/999/
```

**Resultado esperado:** respuesta HTTP 404 controlada.

### Prueba 5: Estados

**Acción:** utilizar datos cuyo consumo total sea menor, igual y mayor que el límite de la zona.

**Resultado esperado:**

```text
consumo_total <= limite_kwh → NORMAL
consumo_total > limite_kwh  → ALERTA
```

---

## 9. Integración MVT

La aplicación utiliza la arquitectura MVT de Django.

### Model

En esta fase los datos no utilizan Models ni ORM. La información se obtiene directamente desde los archivos JSON.

### View

Las Views realizan la carga, búsqueda, filtrado, relación y cálculo de los datos antes de enviarlos al Template.

### Template

Los Templates reciben los datos procesados y se encargan de presentar la información mediante HTML y Bootstrap.

Flujo general:

```text
JSON
 ↓
Views
 ↓
Procesamiento y relaciones en Python
 ↓
Contexto
 ↓
Templates
 ↓
Interfaz web
```

---

## 10. Conclusión

El análisis permite identificar que el funcionamiento principal de EcoEnergy depende de las relaciones entre zonas, categorías y dispositivos.

El procesamiento se realiza dinámicamente para permitir que la aplicación continúe funcionando cuando aumente la cantidad de registros, cuando una zona no tenga dispositivos o cuando se consulte un identificador inexistente.
