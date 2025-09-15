# /services/auth.py

import requests

def obtener_token(usuario, clave, url_auth):
    payload = {
        "username": usuario,
        "password": clave
    }

    try:
        response = requests.post(url_auth, json=payload)
        response.raise_for_status()
        return response.json().get("token")
    except requests.RequestException as e:
        raise Exception(f"Error al autenticar: {e}")
