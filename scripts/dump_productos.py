"""Vuelco seguro de la base Cairos: SOLO productos y mecanica de promos.

Por seguridad NO incluye:

    usuario, bodega, ruta, entrega, Empleado, empleadoAsignado,
    orden, ordenProducto, ordenPromocion, ventasDirectas,
    ventaProducto, ventaPromocion, ni cualquier historial que pueda
    contener datos personales o financieros.

Las credenciales se leen del entorno o de un archivo .env:

    MYSQL_HOST     - IP o hostname del MySQL        (obligatorio)
    MYSQL_USER     - Usuario MySQL                  (obligatorio)
    MYSQL_PASSWORD - Contrasena MySQL               (obligatorio)
    MYSQL_DB       - Nombre de la base              (default: Cairos)
    OUTPUT_FILE    - Ruta del SQL generado          (default: db/dump_cairos_productos.sql)
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Iterable

from dotenv import load_dotenv

try:
    import mysql.connector
except ImportError:
    print(
        "Falta la dependencia mysql-connector-python. "
        "Instala con: pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise

# Tablas que SÍ se vuelcan (solo productos y promos, sin datos sensibles).
TABLAS_PRODUCTO = (
    "producto",
    "precioProducto",
    "almacen",
    "promocion",
    "promocionPorcentual",
    "promocionBogo",
)

# Tablas EXCLUIDAS explicitas por seguridad.
TABLAS_EXCLUIDAS = (
    "usuario",
    "bodega",
    "ruta",
    "entrega",
    "Empleado",
    "empleadoAsignado",
    "orden",
    "ordenProducto",
    "ordenPromocion",
    "ventasDirectas",
    "ventaProducto",
    "ventaPromocion",
)

load_dotenv()


def sql_escape(value) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    value = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{value}'"


def table_exists(cursor, name: str) -> bool:
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = %s AND table_name = %s",
        (os.getenv("MYSQL_DB"), name),
    )
    return cursor.fetchone()[0] > 0


def dump_table(cursor, table: str, lines: list[str]) -> int:
    if not table_exists(cursor, table):
        lines.append(f"-- tabla omitida (no existe): {table}")
        return 0

    cursor.execute(f"SELECT * FROM `{table}`")
    rows = cursor.fetchall()
    if not rows:
        lines.append(f"-- tabla omitida (vacia): {table}")
        return 0

    col_names = [d[0] for d in cursor.description]
    lines.append("")
    lines.append(f"-- =====================================================")
    lines.append(f"-- {table}: {len(rows)} filas")
    lines.append(f"-- =====================================================")
    lines.append(f"INSERT INTO `{table}` ({', '.join('`' + c + '`' for c in col_names)}) VALUES")

    values_sql: list[str] = []
    for row in rows:
        values_sql.append("    (" + ", ".join(sql_escape(v) for v in row) + ")")
    lines.append(",\n".join(values_sql) + ";")
    return len(rows)


def build_dump(host: str, user: str, password: str, db: str, output: str) -> int:
    conn = mysql.connector.connect(host=host, user=user, password=password, database=db)
    cursor = conn.cursor()

    lines: list[str] = []
    lines.append("-- Cairos - dump parcial (solo productos y promos)")
    lines.append(f"-- generado: {datetime.utcnow().isoformat()}Z")
    lines.append(f"-- base: {db}")
    lines.append("--")
    lines.append("-- Tablas volcadas:")
    for t in TABLAS_PRODUCTO:
        lines.append(f"--   + {t}")
    lines.append("--")
    lines.append("-- Tablas EXCLUIDAS (por seguridad, no se vuelcan):")
    for t in TABLAS_EXCLUIDAS:
        lines.append(f"--   - {t}")

    total = 0
    for table in TABLAS_PRODUCTO:
        total += dump_table(cursor, table, lines)

    cursor.close()
    conn.close()

    with open(output, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"Dump escrito en {output}. Filas totales: {total}.")
    return total


def main(argv: Iterable[str]) -> int:
    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    db = os.getenv("MYSQL_DB", "Cairos")
    output = os.getenv("OUTPUT_FILE", "db/dump_cairos_productos.sql")

    if not (host and user and password):
        print(
            "Faltan variables MYSQL_HOST, MYSQL_USER o MYSQL_PASSWORD. "
            "Defínelas en el entorno o en un .env",
            file=sys.stderr,
        )
        return 1

    return 0 if build_dump(host, user, password, db, output) >= 0 else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
