# Cairos Extra

Herramientas auxiliares del proyecto. Incluye un servidor HTTP stub
para integración con WhatsApp y un script que genera un dump limpio
de la base de datos de productos (sin datos de usuarios ni pedidos).

## Servidor

    pip install -r requirements.txt
    python main.py

## Dump DB

    python scripts/dump_productos.py