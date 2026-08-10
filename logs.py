import os
from datetime import datetime

CARPETA_LOGS = "logs"
ARCHIVO_LOG = "eventos.log"


def registrar_evento(mensaje):
    if not os.path.exists(CARPETA_LOGS):
        os.makedirs(CARPETA_LOGS)
    ruta = os.path.join(CARPETA_LOGS, ARCHIVO_LOG)
    momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write("[" + momento + "] " + mensaje + "\n")
    except Exception as error:
        print("No se pudo escribir en el log:", error)