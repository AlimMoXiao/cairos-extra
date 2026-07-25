# Cairos Extra

Repositorio de herramientas auxiliares del **proyecto Cairos**. Aqui no
hay codigo de las apps moviles (esas viven en cairos-bodega y
cairos-transporte). Solo se guardan funciones de backend que necesitan
compartir tanto el equipo de desarrollo como otras instalaciones.

## Que hay aqui

### 1. Servidor HTTP auxiliar (main.py)

Pequeno servidor FastAPI que expone dos endpoints:

| Endpoint | Metodo | Descripcion |
|---|---|---|
| `/health` | GET | Comprobacion de vida del servicio |
| `/enviar` | POST | Registra un mensaje y responde 200 |

El endpoint `/enviar` recibe:

```json
{
  "numero": "51999999999",
  "mensaje": "Su pedido ha sido entregado.",
  "hora": "now"
}
```

Por ahora es un **stub**: valida el payload, lo loguea y responde 200.
La integracion real con un proveedor de WhatsApp (Meta Cloud API,
Baileys, whatsapp-web.js, etc.) se implementa dentro de la funcion
`_enviar_whatsapp()` en `main.py` sin tocar la API publica.

Para correrlo:

```bash
pip install -r requirements.txt
cp .env.example .env      # editame con las credenciales reales
python main.py
```

El servidor escucha en el puerto indicado por `WSP_PORT` (default 5001).

### 2. Dump seguro de la base de datos (scripts/dump_productos.py)

Genera un archivo SQL que contiene **unicamente** las tablas
relacionadas con el catalogo de productos y la mecanica de promociones.
No contiene datos de usuarios, bodegas, ordenes ni informacion personal.

**Tablas que SÍ incluye:**
`producto`, `precioProducto`, `almacen`, `promocion`,
`promocionPorcentual`, `promocionBogo`

**Tablas EXCLUIDAS por seguridad:**
`usuario`, `bodega`, `ruta`, `entrega`, `Empleado`,
`empleadoAsignado`, `orden`, `ordenProducto`, `ordenPromocion`,
`ventasDirectas`, `ventaProducto`, `ventaPromocion`

Para regenerar el dump:

```bash
pip install -r requirements.txt
cp .env.example .env    # MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
python scripts/dump_productos.py
```

El resultado queda en `db/dump_cairos_productos.sql`.

## Archivos

```
cairos-extra/
├── main.py                        # Servidor FastAPI (stub WS)
├── requirements.txt
├── .env.example                   # Template de variables de entorno
├── .gitignore
├── README.md                      # Este archivo
├── scripts/
│   └── dump_productos.py          # Generador del dump SQL parcial
└── db/
    ├── dump_cairos_productos.sql  # Dump base (estructura sin datos)
    └── README.md                  # Instrucciones de regeneracion
```

## Variables de entorno

Definidas en `.env` (copiado de `.env.example`):

| Variable | Descripcion | Default |
|---|---|---|
| `MYSQL_HOST` | IP del servidor MySQL | 192.168.0.0 |
| `MYSQL_USER` | Usuario MySQL | CairosUser |
| `MYSQL_PASSWORD` | Contrasena MySQL | CONTRASENA |
| `MYSQL_DB` | Nombre de la base | Cairos |
| `WSP_PORT` | Puerto del servidor HTTP | 5001 |

## Requisitos

- Python 3.11 o superior
- MySQL/MariaDB con la base `Cairos` populada
- Las dependencias de `requirements.txt`

## Nota

El nombre "Cairos" es un identificador temporal del proyecto. No
representa ninguna empresa ni entidad legal existente.
