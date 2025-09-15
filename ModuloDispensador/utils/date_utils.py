from datetime import datetime, timedelta

def generar_rango_fechas(fecha_inicio, fecha_fin):
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    delta = (fin - inicio).days + 1
    return [(inicio + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta)]
