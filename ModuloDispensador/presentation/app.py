# /presentation/app.py

import tkinter as tk
from tkinter import PhotoImage
import os
from presentation.components.menu import build_menu
from tkinter import messagebox
from business_logic.direccionamiento import process_put_programacion, process_put_entrega, process_put_reporte_entrega, process_put_reporte_facturacion, process_reporteador_direccionamientos_por_prescripcion, process_direccionamientos_totales
from utils.helpers import get_input, get_excel_file
from tkinter import messagebox
from business_logic.direccionamiento import process_reporteador


temp_img = {}  # Diccionario temporal para evitar que las imágenes sean eliminadas por el garbage collector

class Application:
    def __init__(self, master):
        self.master = master
        master.title("Modulo DISPENSADOR-PROVEEDOR")
        
        # Crear la barra de menú usando build_menu
        callbacks = {
            "direccionamientos": self.direccionamientos_totales,
            "programacion": self.programacion,
            "entrega": self.entrega,
            "reporte_entrega": self.reporte_entrega,
            "reporte_facturacion": self.reporte_facturacion,
            "reporteador_direccionamientos": self.Reporteador_Direccionamientos,
            "reporteador": self.Reporteador,
            "anular_programacion": self.Anular_Programacion,
            "anular_entrega": self.Anular_Entrega,
            "anular_reporte_entrega": self.Anular_ReporteEntrega,
            "anular_facturacion": self.Anular_Facturacion,
            "mostrar_instrucciones": self.mostrar_instrucciones,
        }
        build_menu(master, callbacks)
        
        # Textos informativos
        textos_info = [
            "BIENVENIDO MODULO DISPENSADOR-PROVEEDOR",
            "MIPRES, es una herramienta tecnológica dispuesta por el Ministerio de Salud y Protección Social (MSPS) para garantizar el acceso",
            "De reporte de prescripción, suministro, verificación, control, pago y análisis de la información de las tecnologías en salud.",
            "La Resolución 1885 de 2018 establece el suministro efectivo de las tecnologías en salud y de los servicios ",
            "complementarios por parte de los proveedores",
            "Para iniciar por favor seleccione un proceso del menú"
        ]

        for texto in textos_info:
            info_label = tk.Label(master, text=texto, justify="center", font=("TkDefaultFont", 9, "bold"))
            info_label.pack(pady=3)
        
        # Cargar imágenes
        self.cargar_imagenes()

    def cargar_imagenes(self):
        """Carga las imágenes desde la carpeta assets."""
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        try:
            img_files = ["logo.png", "minsalud.png"]
            for i, img_file in enumerate(img_files):
                img_path = os.path.join(assets_dir, img_file)
                if os.path.exists(img_path):
                    temp_img[f"logo_{i}"] = PhotoImage(file=img_path).subsample(3, 3)
                    label = tk.Label(self.master, image=temp_img[f"logo_{i}"])
                    label.pack(side="top", padx=3, pady=3)
        except Exception as e:
            print(f"Error al cargar imágenes: {e}")
    
    def quit(self):
        """Cierra la aplicación."""
        self.master.quit()
    
    # Métodos de procesos (placeholder)

    def direccionamientos_totales(self):
        token = get_input("Ingrese el token:")
        fecha_inicio = get_input("Ingrese la fecha de inicio (YYYY-MM-DD):")
        fecha_fin = get_input("Ingrese la fecha de fin (YYYY-MM-DD):")
        ruta_archivo = get_excel_file()

        try:
            process_direccionamientos_totales(token, fecha_inicio, fecha_fin, ruta_archivo)
            messagebox.showinfo("Sispro API", f"Los datos se han guardado exitosamente en el archivo: {ruta_archivo}")
        except FileNotFoundError:
            messagebox.showerror("Sispro API", f"No se encontró el archivo: {ruta_archivo}")
        except Exception as e:
            messagebox.showerror("Sispro API", f"Error inesperado: {e}")

    def programacion(self):
        token = get_input("Ingrese el token:")
        archivo = get_excel_file()
        try:
            process_put_programacion(token, archivo)
            messagebox.showinfo("PUT Programación", "Proceso finalizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error en PUTProgramacion", str(e))
            
    def entrega(self):
        token = get_input("Ingrese el token:")
        archivo_excel = get_excel_file()
        try:
            process_put_entrega(token, archivo_excel)        
            messagebox.showinfo("Sispro API", "Entrega procesada correctamente.")
        except FileNotFoundError:
            messagebox.showerror("Sispro API", "No se pudo encontrar el archivo seleccionado.")
        except Exception as e:
            messagebox.showerror("Sispro API", f"Ocurrió un error: {str(e)}")
            
    def reporte_entrega(self):
        token = get_input("Ingrese el token:")
        archivo_excel = get_excel_file()

        try:
            process_put_reporte_entrega(token, archivo_excel)
            messagebox.showinfo("Sispro API", "Reporte de entrega procesado correctamente.")
        except FileNotFoundError:
            messagebox.showerror("Sispro API", "No se encontró el archivo.")
        except Exception as e:
            messagebox.showerror("Sispro API", f"Error inesperado: {str(e)}")

    def reporte_facturacion(self):
            
        token = get_input("Ingrese el token:")
        archivo_excel = get_excel_file()
        try:
            process_put_reporte_facturacion(token, archivo_excel)
            messagebox.showinfo("Sispro API", "Reporte de facturación procesado correctamente.")
        except FileNotFoundError:
            messagebox.showerror("Sispro API", "No se encontró el archivo.")
        except Exception as e:
            messagebox.showerror("Sispro API", f"Error inesperado: {str(e)}")


    def Reporteador_Direccionamientos(self):
        token = get_input("Ingrese el token:")
        archivo_excel = get_excel_file()
        try:
            process_reporteador_direccionamientos_por_prescripcion(token, archivo_excel)

            messagebox.showinfo("Sispro API", "Reporteador de direccionamientos completado.")
        except Exception as e:
            messagebox.showerror("Sispro API", f"Ocurrió un error: {e}")

    def Reporteador(self):

        token = get_input("Ingrese el token:")
        archivo_excel = get_excel_file()
        try:
            # 1. Pedir token y archivo Exce
            # 2. Llamar al proceso centralizado
            process_reporteador(token, archivo_excel)

            # 3. Confirmación al usuario
            from tkinter import messagebox
            messagebox.showinfo("Sispro API", "El Reporteador se ejecutó correctamente y los datos se guardaron en el Excel.")

        except Exception as e:
            import logging
            logging.error(f"Error al ejecutar el Reporteador: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar el Reporteador:\n{str(e)}")

    def Anular_Programacion(self): pass


    def Anular_Entrega(self): pass
    def Anular_ReporteEntrega(self): pass
    def Anular_Facturacion(self): pass
    def mostrar_instrucciones(self): pass