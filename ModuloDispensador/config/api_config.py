# /config/api_config.py

BASE_URL = "https://wsmipres.sispro.gov.co/WSSUMMIPRESNOPBS/api"
BASE_URL_FACTURACION = "https://wsmipres.sispro.gov.co/WSFACMIPRESNOPBS/api"
NIT_PROVEEDOR = "900381555"

ENDPOINTS = {
    "direccionamiento_por_fecha": f"{BASE_URL}/DireccionamientoXFecha/{NIT_PROVEEDOR}",
    "programacion": f"{BASE_URL}/Programacion/{NIT_PROVEEDOR}",
    "entrega": f"{BASE_URL}/Entrega/{NIT_PROVEEDOR}",
    "reporte_entrega": f"{BASE_URL}/ReporteEntrega/{NIT_PROVEEDOR}",
    "reporte_facturacion": f"{BASE_URL_FACTURACION}/ReporteFacturacion/{NIT_PROVEEDOR}",
    "direccionamiento_por_prescripcion": f"{BASE_URL}/DireccionamientoXPrescripcion/{NIT_PROVEEDOR}",
    # Agregamos más en el futuro si hace falta
}

HEADERS_TEMPLATE = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    # Authorization lo agregamos dinámicamente en api_client.py
}

# Endpoints usados específicamente para el Reporteador
ENDPOINTS_REPORTEADOR = {
    "ProgramacionXPrescripcion": "https://wsmipres.sispro.gov.co/WSSUMMIPRESNOPBS/api/ProgramacionXPrescripcion",
    "EntregaXPrescripcion": "https://wsmipres.sispro.gov.co/WSSUMMIPRESNOPBS/api/EntregaXPrescripcion",
    "ReporteEntregaXPrescripcion": "https://wsmipres.sispro.gov.co/WSSUMMIPRESNOPBS/api/ReporteEntregaXPrescripcion",
    "FacturacionXPrescripcion": "https://wsmipres.sispro.gov.co/WSFACMIPRESNOPBS/api/FacturacionXPrescripcion",
}
