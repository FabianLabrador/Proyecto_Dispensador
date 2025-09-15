# /data_access/config.py

API_URL_DIRECCIONAMIENTO = "https://api.sispro.gov.co/v1/direccionamiento"
API_TIMEOUT = 10  # segundos
MAX_WORKERS = 5

COLUMNAS_REQUERIDAS = [
    "ID_SERVICIO", "FECHA", "PACIENTE", "DIAGNOSTICO", "IPS_DESTINO"
]
