# /utils/logging_setup.py

import logging
import os

def setup_logging(nombre_logger="direccionamiento"):
    logger = logging.getLogger(nombre_logger)
    logger.setLevel(logging.INFO)

    os.makedirs("logs", exist_ok=True)
    archivo_log = os.path.join("logs", "modulo_direccionamiento.log")

    fh = logging.FileHandler(archivo_log)
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger
