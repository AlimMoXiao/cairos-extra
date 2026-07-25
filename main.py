"""Servidor HTTP auxiliar del proyecto Cairos.

Por ahora expone solo dos endpoints:

    GET  /health              -> comprobacion de vida
    POST /enviar   {numero, mensaje, hora}
                              -> registra el mensaje y responde 200

El endpoint /enviar es un stub: NO envia el WhatsApp de verdad, solo
valida el payload y lo loguea. Cuando se integre con un proveedor real
(Meta Cloud API, Baileys, whatsapp-web.js, etc.) se reemplaza la
funcion _enviar_whatsapp sin tocar la API publica.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

WSP_PORT = int(os.getenv("WSP_PORT", "5001"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("cairos-extra")

app = FastAPI(
    title="Cairos Extra",
    description="Servidor HTTP auxiliar del proyecto Cairos.",
    version="0.1.0",
)


class EnviarPayload(BaseModel):
    numero: str = Field(..., min_length=4, max_length=32)
    mensaje: str = Field(..., min_length=1, max_length=4096)
    hora: Optional[str] = Field(default=None, description="ISO o 'now'")


class EnviarResponse(BaseModel):
    enviado: bool
    recibido: EnviarPayload
    timestamp: str


def _enviar_whatsapp(numero: str, mensaje: str) -> bool:
    """Stub de envio.

    Devuelve True cuando se considera enviado. La integracion real con
    un proveedor de WhatsApp se hace aca, sin tocar la API publica.
    """
    log.info("STUB enviar numero=%s mensaje_len=%d", numero, len(mensaje))
    return True


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/enviar", response_model=EnviarResponse)
def enviar(payload: EnviarPayload) -> EnviarResponse:
    hora = payload.hora or "now"

    try:
        ok = _enviar_whatsapp(payload.numero, payload.mensaje)
    except Exception as exc:  # pragma: no cover - solo log
        log.exception("Fallo al intentar enviar WhatsApp")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if not ok:
        raise HTTPException(status_code=502, detail="No se pudo enviar el mensaje")

    log.info("OK enviar numero=%s hora=%s", payload.numero, hora)

    return EnviarResponse(
        enviado=True,
        recibido=payload,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=WSP_PORT, reload=False)
