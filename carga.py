import cvs
import os



def cargar_telemetria(ruta_archivo: str) -> list[dict]:
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError("No se encuentra el archivo")
    else:
        with open(ruta_archivo, "r", newline="", encode="utf-8", as f)
        lector = csv.DictReader(f, delimiter=",")
        for columna in lector:
            print("Fila", )
