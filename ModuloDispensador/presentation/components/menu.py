# /presentation/gui_components/menu.py

import tkinter as tk

def build_menu(master, callbacks):
    """
    Construye la barra de menú principal de la aplicación.
    
    :param master: La ventana principal de la aplicación.
    :param callbacks: Un diccionario con las funciones correspondientes a cada opción del menú.
    """
    menu_bar = tk.Menu(master)
    
    # Menú de procesos
    processes_menu = tk.Menu(menu_bar, tearoff=0)
    processes_menu.add_command(label="Direccionamientos Totales", command=callbacks.get("direccionamientos", lambda: None))
    processes_menu.add_command(label="PUTProgramacion", command=callbacks.get("programacion", lambda: None))
    processes_menu.add_command(label="PUTEntrega", command=callbacks.get("entrega", lambda: None))
    processes_menu.add_command(label="PUTReporte Entrega", command=callbacks.get("reporte_entrega", lambda: None))
    processes_menu.add_command(label="PUTReporte Facturacion", command=callbacks.get("reporte_facturacion", lambda: None))
    processes_menu.add_command(label="Reporteador Direccionamiento", command=callbacks.get("reporteador_direccionamientos", lambda: None))
    processes_menu.add_command(label="Reporteador", command=callbacks.get("reporteador", lambda: None))
    processes_menu.add_command(label="AnularProgramacion", command=callbacks.get("anular_programacion", lambda: None))
    processes_menu.add_command(label="AnularEntrega", command=callbacks.get("anular_entrega", lambda: None))
    processes_menu.add_command(label="AnularReporteEntrega", command=callbacks.get("anular_reporte_entrega", lambda: None))
    processes_menu.add_command(label="AnularFacturacion", command=callbacks.get("anular_facturacion", lambda: None))
    menu_bar.add_cascade(label="Proceso", menu=processes_menu)
    
    # Menú de ayuda
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Instrucciones", command=callbacks.get("mostrar_instrucciones", lambda: None))
    menu_bar.add_cascade(label="Ayuda", menu=help_menu)
    
    # Menú de salida
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Salir", command=master.quit)
    menu_bar.add_cascade(label="Salir", menu=file_menu)
    
    master.config(menu=menu_bar)