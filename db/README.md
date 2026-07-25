# Base de datos — Dump parcial de Cairos

Este directorio contiene un dump SQL de la base `Cairos` que incluye
**unicamente** las tablas de productos y la mecanica de promociones.

## Tablas incluidas

| Tabla | Contenido |
|---|---|
| `producto` | Catalogo: nombre, marca, categoria, descripcion, status |
| `precioProducto` | Historial de precios (precioBase, precioVenta, precioSugerido) por fecha |
| `almacen` | Inventario por almacen (referencia de nombres, sin datos sensibles) |
| `promocion` | Promociones activas y su estado |
| `promocionPorcentual` | Promociones de descuento porcentual con monto minimo de compra |
| `promocionBogo` | Promociones compra-unidad-regalo-unidad (tipo 'compra' y 'regalo') |

## Tablas excluidas (por seguridad)

`usuario`, `bodega`, `ruta`, `entrega`, `Empleado`,
`empleadoAsignado`, `orden`, `ordenProducto`, `ordenPromocion`,
`ventasDirectas`, `ventaProducto`, `ventaPromocion`.

Ninguna de las tablas excluidas se volca en este directorio, ni en
forma de datos ni de estructura.

## Como regenerar el dump

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar el archivo `.env` (copiado de `.env.example`) con las
   credenciales de la base de datos.

3. Ejecutar:
   ```bash
   python scripts/dump_productos.py
   ```

El script se conecta a MySQL, vuelca las 6 tablas de producto y genera
el archivo `dump_cairos_productos.sql` en este directorio.

## Contenido del archivo SQL

El archivo generado por `dump_productos.py` es un conjunto de
sentencias `INSERT INTO` con todas las filas de las tablas incluidas.
Si la base no existe o alguna tabla esta vacia, el script la omite y
deja un comentario en el SQL.

El archivo `dump_cairos_productos.sql` que vive aqui es la version base:
contiene la estructura (CREATE TABLE si aplica) pero sin datos reales.
Una ejecucion normal de `dump_productos.py` lo sobreescribe con la
informacion vigente.
