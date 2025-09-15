# /business_logic/batch_processing.py

import concurrent.futures
import time
from services.api_client import enviar_lote

MAX_REINTENTOS = 3

def procesar_en_lotes(servicios, token):
    resultados = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futuros = {
            executor.submit(intentar_envio, lote, token): lote for lote in servicios
        }

        for futuro in concurrent.futures.as_completed(futuros):
            try:
                resultado = futuro.result()
                resultados.append(resultado)
            except Exception as e:
                resultados.append(f"Error: {e}")

    return resultados

def intentar_envio(lote, token):
    for intento in range(MAX_REINTENTOS):
        respuesta = enviar_lote(lote, token)
        if respuesta.get("estado") == "exitoso":
            return respuesta
        time.sleep(1)  # Espera antes del siguiente intento
    return {"estado": "fallido", "mensaje": "Todos los reintentos fallaron"}
