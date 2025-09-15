# /business_logic/direccionamiento.py

from services.api_client import obtener_direccionamiento_por_fecha
from utils.date_utils import generar_rango_fechas
from concurrent.futures import ThreadPoolExecutor
from data_access.excel_handler import cargar_datos_excel, guardar_respuestas_en_excel,guardar_direccionamientos_en_excel
from services.api_client import enviar_concurrente
from config.api_config import ENDPOINTS
import time
import logging
from services.api_client import obtener_direccionamiento_por_prescripcion
from data_access.excel_handler import guardar_reporte_direccionamientos_por_prescripcion
import pandas as pd
from data_access.excel_handler import cargar_datos_entrega, guardar_respuestas_en_excel
from services.api_client import enviar_concurrente
from config.api_config import ENDPOINTS
from services.api_client import obtener_concurrente
from data_access.excel_handler import guardar_reporte_combinado_en_excel
from config.api_config import ENDPOINTS_REPORTEADOR
from services.api_client import obtener_concurrente
from data_access.excel_handler import guardar_reporte_direccionamientos_por_prescripcion
import pandas as pd 
def process_direccionamientos_totales(token, fecha_inicio, fecha_fin, ruta_archivo):
    fechas = generar_rango_fechas(fecha_inicio, fecha_fin)
    informacion_total = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados = executor.map(lambda fecha: obtener_direccionamiento_por_fecha(fecha, token), fechas)

    for resultado in resultados:
        if resultado:
            informacion_total.extend(resultado)

    if informacion_total:
        guardar_direccionamientos_en_excel(informacion_total, ruta_archivo)
    else:
        raise ValueError("No se obtuvo información de la API.")

    
# /business_logic/direccionamiento.py

def construir_payload_programacion(row):
    """
    Construye el payload de programación a partir de una fila del DataFrame.
    """
    from pandas import to_datetime

    return {
        "ID": row['ID'],
        "FecMaxEnt": to_datetime(row['FecMaxEnt']).strftime('%Y-%m-%d'),
        "TipoIDSedeProv": str(row['TipoIDSedeProv']),
        "NoIDSedeProv": str(row['NoIDSedeProv']),
        "CodSedeProv": str(row['CodSedeProv']),
        "CodSerTecAEntregar": str(row['CodSerTecAEntregar']),
        "CantTotAEntregar": str(row['CantTotAEntregar']),
    }

def process_put_programacion(token, archivo_excel):
    """
    Carga datos del Excel, construye los payloads y realiza el envío concurrente optimizado.
    """
    # 1. Cargar datos desde Excel
    df = cargar_datos_excel(archivo_excel)

    # 2. Construir los payloads
    payloads = [construir_payload_programacion(row) for _, row in df.iterrows()]

    # 3. Construir URL final con token
    url_api = f"{ENDPOINTS['programacion']}/{token}"

    # 4. Enviar concurrentemente usando versión optimizada
    respuestas = enviar_concurrente(payloads, url_api, token, metodo='PUT', pausa=0.05)

    # 5. Guardar respuestas en la hoja "Programacion"
    guardar_respuestas_en_excel(df, respuestas, archivo_excel,"Programacion")



def construir_payload_entrega(row):
    return {
        "ID": row['ID'] if pd.notnull(row['ID']) else '',
        "CodSerTecEntregado": str(row['CodSerTecEntregado']) if pd.notnull(row['CodSerTecEntregado']) else '',
        "CantTotEntregada": str(row['CantTotEntregada']) if pd.notnull(row['CantTotEntregada']) else '',
        "EntTotal": int(row['EntTotal']) if pd.notnull(row['EntTotal']) else '',
        "CausaNoEntrega": int(row['CausaNoEntrega']) if pd.notnull(row['CausaNoEntrega']) else '',
        "FecEntrega": pd.to_datetime(row['FecEntrega']).strftime('%Y-%m-%d') if pd.notnull(row['FecEntrega']) else '',
        "NoLote": str(row['NoLote']) if pd.notnull(row['NoLote']) else '',
        "TipoIDRecibe": str(row['TipoIDRecibe']) if pd.notnull(row['TipoIDRecibe']) else '',
        "NoIDRecibe": str(row['NoIDRecibe']) if pd.notnull(row['NoIDRecibe']) else '',
    }

def process_put_entrega(token, archivo_excel):
    df = cargar_datos_entrega(archivo_excel)
    payloads = [construir_payload_entrega(row) for _, row in df.iterrows()]
    
    url_api = f"{ENDPOINTS['entrega']}/{token}"
    respuestas = enviar_concurrente(payloads, url_api, token)
    
    guardar_respuestas_en_excel(df, respuestas, archivo_excel, "Entrega")

def construir_payload_reporte_entrega(row):
    return {
        "ID": row['ID'] if pd.notnull(row['ID']) else '',
        "FecRepEntrega": pd.to_datetime(row['FecRepEntrega']).strftime('%Y-%m-%d') if pd.notnull(row['FecRepEntrega']) else '',
        "TipoIDReporta": str(row['TipoIDReporta']) if pd.notnull(row['TipoIDReporta']) else '',
        "NoIDReporta": str(row['NoIDReporta']) if pd.notnull(row['NoIDReporta']) else ''
    }

def process_put_reporte_entrega(token, archivo_excel):
    df = pd.read_excel(archivo_excel, sheet_name='ReporteEntrega')
    payloads = [construir_payload_reporte_entrega(row) for _, row in df.iterrows()]
    
    from config.api_config import ENDPOINTS
    from services.api_client import enviar_concurrente
    from data_access.excel_handler import guardar_respuestas_en_excel

    url_api = f"{ENDPOINTS['reporte_entrega']}/{token}"
    respuestas = enviar_concurrente(payloads, url_api, token)
    
    guardar_respuestas_en_excel(df, respuestas, archivo_excel, "ReporteEntrega")

def construir_payload_reporte_facturacion(row):
    return {
        "ID": row['ID'] if pd.notnull(row['ID']) else '',
        "FecRepFacturacion": pd.to_datetime(row['FecRepFacturacion']).strftime('%Y-%m-%d') if pd.notnull(row['FecRepFacturacion']) else '',
        "TipoIDReporta": str(row['TipoIDReporta']) if pd.notnull(row['TipoIDReporta']) else '',
        "NoIDReporta": str(row['NoIDReporta']) if pd.notnull(row['NoIDReporta']) else ''
    }

def process_put_reporte_facturacion(token, archivo_excel):
    df = pd.read_excel(archivo_excel, sheet_name='ReporteFacturacion')
    payloads = [construir_payload_reporte_facturacion(row) for _, row in df.iterrows()]
    
    from config.api_config import ENDPOINTS
    from services.api_client import enviar_concurrente
    from data_access.excel_handler import guardar_respuestas_en_excel

    url_api = f"{ENDPOINTS['reporte_facturacion']}/{token}"
    respuestas = enviar_concurrente(payloads, url_api, token)
    
    guardar_respuestas_en_excel(df, respuestas, archivo_excel, "ReporteFacturacion")

def process_reporteador_direccionamientos_por_prescripcion(token, ruta_archivo):
    import pandas as pd
    df = pd.read_excel(ruta_archivo)
    ids_prescripcion = df['Mipres'].dropna().astype(str).tolist()

    encabezados = [
        "ID", "IDDireccionamiento", "NoPrescripcion", "TipoTec", "ConTec", "TipoIDPaciente",
        "NoIDPaciente", "NoEntrega", "NoSubEntrega", "TipoIDProv", "NoIDProv",
        "CodMunEnt", "FecMaxEnt", "CantTotAEntregar",
        "DirPaciente", "CodSerTecAEntregar", "NoIDEPS", "CodEPS",
        "FecDireccionamiento", "EstDireccionamiento", "FecAnulacion"
    ]

    resultados = []

    for id_prescripcion in ids_prescripcion:
        datos = obtener_direccionamiento_por_prescripcion(token, id_prescripcion)
        if isinstance(datos, list) and datos:
            resultados.append(datos)
        time.sleep(0.2)

    if resultados:
        guardar_reporte_direccionamientos_por_prescripcion(
            resultados=resultados,
            ruta_archivo=ruta_archivo,
            hoja_nombre="DireccionamientoXPrescripcion",
            encabezados=encabezados
        )
    else:
        raise ValueError("No se encontraron resultados para los IDs proporcionados.")

def process_reporteador_direccionamientos_por_prescripcion(token, ruta_archivo):
    import pandas as pd
    df = pd.read_excel(ruta_archivo)
    ids_prescripcion = df['Mipres'].dropna().astype(str).tolist()

    encabezados = [
        "ID", "IDDireccionamiento", "NoPrescripcion", "TipoTec", "ConTec", "TipoIDPaciente",
        "NoIDPaciente", "NoEntrega", "NoSubEntrega", "TipoIDProv", "NoIDProv",
        "CodMunEnt", "FecMaxEnt", "CantTotAEntregar",
        "DirPaciente", "CodSerTecAEntregar", "NoIDEPS", "CodEPS",
        "FecDireccionamiento", "EstDireccionamiento", "FecAnulacion"
    ]

    from services.api_client import obtener_concurrente, obtener_direccionamiento_por_prescripcion
    from data_access.excel_handler import guardar_reporte_direccionamientos_por_prescripcion

    resultados = obtener_concurrente(ids_prescripcion, obtener_direccionamiento_por_prescripcion, token)

    if resultados:
        guardar_reporte_direccionamientos_por_prescripcion(
            resultados=resultados,
            ruta_archivo=ruta_archivo,
            hoja_nombre="DireccionamientoXPrescripcion",
            encabezados=encabezados
        )
    else:
        raise ValueError("No se encontraron resultados para los IDs proporcionados.")
    
def process_reporteador(token, archivo_excel, max_workers=10):
    """
    Consulta varios endpoints (ProgramacionXPrescripcion, EntregaXPrescripcion,
    ReporteEntregaXPrescripcion, FacturacionXPrescripcion) y guarda los resultados
    en hojas separadas dentro del mismo archivo Excel.
    """

    df = pd.read_excel(archivo_excel)
    ids_prescripcion = df['Mipres'].dropna().astype(str).tolist()

    for endpoint, cfg in ENDPOINTS_REPORTEADOR.items():
        url_base = cfg["url"]
        headers_endpoint = cfg["headers"]

        # 1. Construir URLs
        urls = [f"{url_base}/{token}/{mipres_id}" for mipres_id in ids_prescripcion]

        logging.info(f"Consultando {endpoint} con {len(urls)} solicitudes...")

        # 2. Ejecutar concurrentemente
        resultados = obtener_concurrente(urls, max_workers=max_workers)

        # 3. Filtrar respuestas válidas
        resultados_limpios = []
        for r in resultados:
            if r and isinstance(r, list):
                resultados_limpios.extend(r)
            elif r and isinstance(r, dict):  # a veces la API devuelve un solo dict
                resultados_limpios.append(r)

        # 4. Guardar resultados en una hoja con el nombre del endpoint
        if resultados_limpios:
            guardar_reporte_direccionamientos_por_prescripcion(
                resultados=[resultados_limpios],
                ruta_archivo=archivo_excel,
                hoja_nombre=endpoint,
                encabezados=headers_endpoint
            )
        else:
            logging.warning(f"No se obtuvieron resultados para {endpoint}")


def combinar_resultados(resultados_por_endpoint):
    """
    Combina los resultados obtenidos de varios endpoints en una sola estructura.
    Prefija los encabezados con el nombre del endpoint.
    """
    data_dict = {}
    prefixed_headers = []

    for endpoint, lista_respuestas in resultados_por_endpoint.items():
        headers = ENDPOINTS_REPORTEADOR[endpoint]["headers"]

        for header in headers:
            prefixed_headers.append(f"{endpoint}_{header}")

        # 🔎 iteramos cada lista de respuestas
        for response_data in lista_respuestas:
            if not response_data:
                continue
            for record in response_data:
                if not isinstance(record, dict):
                    continue
                record_id = record.get("ID")
                if not record_id:
                    continue
                if record_id not in data_dict:
                    data_dict[record_id] = {}
                for header in headers:
                    data_dict[record_id][f"{endpoint}_{header}"] = record.get(header, "")

    # 🔎 Paso extra: match de Facturación contra Programación
    for record_id, combined_data in list(data_dict.items()):
        if "FacturacionXPrescripcion_IDFacturacion" in combined_data:
            match_found = False
            for other_id, other_data in data_dict.items():
                if other_id != record_id and \
                   combined_data.get("FacturacionXPrescripcion_NoPrescripcion") == other_data.get("ProgramacionXPrescripcion_NoPrescripcion") and \
                   combined_data.get("FacturacionXPrescripcion_NoEntrega") == other_data.get("ProgramacionXPrescripcion_NoEntrega") and \
                   combined_data.get("FacturacionXPrescripcion_ConTec") == other_data.get("ProgramacionXPrescripcion_ConTec") and \
                   combined_data.get("FacturacionXPrescripcion_CodSerTecAEntregado") == other_data.get("ProgramacionXPrescripcion_CodSerTecAEntregar"):
                    data_dict[other_id].update(combined_data)
                    match_found = True
                    break
            if match_found:
                del data_dict[record_id]

    return data_dict, prefixed_headers





