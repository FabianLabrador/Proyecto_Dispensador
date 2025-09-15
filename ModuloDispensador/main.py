# main.py

import sys
import os
import tkinter as tk

# Asegurar que la raíz del proyecto esté en sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from presentation.app import Application
from utils.logging_setup import setup_logging

def main():
    # Configurar logging
    setup_logging()

    # Crear ventana principal
    root = tk.Tk()
    root.title("Módulo Dispensador 2024")
    root.resizable(False, False)  # Evitar redimensionado

    # Cargar la aplicación dentro de la ventana
    app = Application(root)

    # Ejecutar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()
