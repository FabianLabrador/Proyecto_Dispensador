# /services/api_client.py

import requests
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.api_config import HEADERS_TEMPLATE, ENDPOINTS
import multiprocessing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de sesión con reintentos (compartida)
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)


def enviar_a_api(payload, url_api, token, metodo='PUT', max_reintentos=3, pausa=0.05, idx=None):
    """
    Envía un payload individual a la API. Incluye reintentos personalizados, pausa opcional y logs detallados.
    """
    headers = {**HEADERS_TEMPLATE, "Authorization": f"Bearer {token}"}

    for intento in range(1, max_reintentos + 1):
        try:
            time.sleep(pausa)  # Controlar ritmo
            if metodo.upper() == 'PUT':
                response = session.put(url_api, json=payload, headers=headers, timeout=5, verify=False)
            elif metodo.upper() == 'POST':
                response = session.post(url_api, json=payload, headers=headers, timeout=5, verify=False)
            else:
                raise ValueError(f"Método HTTP no soportado: {metodo}")

            if idx is not None:
                print(f"[Fila {idx + 2}] Intento {intento} | Status {response.status_code} - {response.text}")
            else:
                print(f"Payload enviado: {payload}")
                print(f"Respuesta API: {response.status_code} - {response.text}")

            return response

        except requests.RequestException as e:
            logging.warning(f"[{idx + 2 if idx is not None else '?'}] Reintento {intento}: {e}")
            time.sleep(1)

    # Si falla todos los intentos, devolver simulación de error
    class FakeResponse:
        status_code = 0
        text = f"Sin respuesta tras {max_reintentos} intentos"
    return FakeResponse()

# ========================================
# FUNCION GENERAL PARA ENVIAR CONCURRENTE (PARA CUALQUIER PROCESO)
# ========================================
def enviar_concurrente(payloads, url_api, token, metodo='PUT', pausa=0.05):
    """
    Envía múltiples payloads de forma concurrente, con control de errores, pausa y logging.
    """
    respuestas = [''] * len(payloads)
    max_workers = min(50, multiprocessing.cpu_count() * 5)
    logging.info(f"Usando {max_workers} hilos para enviar {len(payloads)} registros...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(enviar_a_api, p, url_api, token, metodo, 3, pausa, i): i
            for i, p in enumerate(payloads)
        }

        for future in as_completed(future_to_index):
            i = future_to_index[future]
            try:
                response = future.result()
                respuestas[i] = f"{response.status_code} - {response.text}"
            except Exception as e:
                respuestas[i] = f"Excepción inesperada: {str(e)}"

    return respuestas

def obtener_direccionamiento_por_prescripcion(token, id_prescripcion):
    from config.api_config import ENDPOINTS

    url = f"{ENDPOINTS['direccionamiento_por_prescripcion']}/{token}/{id_prescripcion}"

    try:
        response = session.get(url, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error {response.status_code} en ID {id_prescripcion}: {response.text}")
            return []
    except requests.RequestException as e:
        logging.error(f"Excepción para ID {id_prescripcion}: {e}")
        return []

def obtener_direccionamiento_por_fecha(fecha, token):
    from config.api_config import ENDPOINTS
    import logging

    url = f"{ENDPOINTS['direccionamiento_por_fecha']}/{token}/{fecha}"

    try:
        response = session.get(url, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error en la fecha {fecha}: {response.status_code} - {response.text}")
            return []
    except requests.RequestException as e:
        logging.error(f"Excepción al solicitar la fecha {fecha}: {e}")
        return []
    

def obtener_concurrente(urls, max_workers=10):
    """
    Realiza múltiples solicitudes GET concurrentes reutilizando una sesión.
    Devuelve siempre respuestas parseadas en JSON (o None si fallan).
    """
    resultados = []

    with requests.Session() as session:
        session.headers.update({'Content-Type': 'application/json'})
        session.verify = False  # evitar errores de certificado, igual que en otros métodos

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(session.get, url): url
                for url in urls
            }

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    response = future.result()
                    response.raise_for_status()
                    try:
                        data = response.json()  # 🔑 siempre JSON
                    except ValueError:
                        logging.error(f"No se pudo parsear JSON desde {url}. Respuesta: {response.text}")
                        data = None
                    resultados.append(data)
                except requests.RequestException as e:
                    logging.error(f"Error en solicitud GET a {url}: {e}")
                    resultados.append(None)

    return resultados



