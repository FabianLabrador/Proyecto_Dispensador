# /presentation/components/logo.py

import tkinter as tk
import os

def build_logo(parent):
    try:
        logo_path = os.path.join("assets", "logo.png")
        logo = tk.PhotoImage(file=logo_path)
        logo_label = tk.Label(parent, image=logo)
        logo_label.image = logo  # Mantener referencia
        logo_label.pack(pady=(0, 20))
    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")
