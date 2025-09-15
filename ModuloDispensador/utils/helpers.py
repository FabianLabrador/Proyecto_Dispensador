# /utils/helpers.py

from tkinter import simpledialog, filedialog

def limpiar_string(valor):
    if isinstance(valor, str):
        return valor.strip().upper()
    return valor

def dividir_en_lotes(lista, tamano):
    for i in range(0, len(lista), tamano):
        yield lista[i:i + tamano]
# /utils/ui_helpers.py

def get_input(prompt: str) -> str:
    """Solicita una cadena de texto al usuario mediante un cuadro de diálogo."""
    return simpledialog.askstring("Entrada requerida", prompt)

def get_excel_file() -> str:
    """Abre un cuadro de diálogo para seleccionar un archivo Excel."""
    return filedialog.askopenfilename(
        title="Seleccionar archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx")]
    )
