import re

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Endereço"])


@router.get("/cep/{cep}")
def lookup_cep(cep: str):
    cep = cep.replace("-", "")
    if not re.fullmatch(r"[0-9]{8}", cep):
        raise HTTPException(422, "Informe um CEP com 8 números.")
    try:
        # Host fixo e CEP numérico impedem que a entrada vire uma URL arbitrária.
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"https://viacep.com.br/ws/{cep}/json/")
            response.raise_for_status()
            address = response.json()
        if not isinstance(address, dict):
            raise ValueError("Resposta inválida")
    except (httpx.HTTPError, ValueError):
        raise HTTPException(502, "ViaCEP indisponível. Preencha o endereço manualmente.")
    if address.get("erro"):
        raise HTTPException(404, "CEP não encontrado.")
    fields = {"cep": "cep", "logradouro": "logradouro", "bairro": "bairro",
              "cidade": "localidade", "estado": "uf"}
    if any(not isinstance(address.get(key, ""), str) for key in fields.values()):
        raise HTTPException(502, "Resposta inválida do ViaCEP.")
    return {key: address.get(source, "") for key, source in fields.items()}
