import csv
import os

def cargar_telemetria(ruta_archivo: str) -> list[dict]:
    if not os.path.exists(ruta_archivo):
        print("No está")
    else:
        with open(ruta_archivo, "r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f, delimiter=",")
            for columna in lector:
                columna["id_sesion"] = int(columna["id_sesion"])
                columna["ping_promedio"] = int(columna["ping_promedio"])
                columna["fps_promedio"] = int(columna["fps_promedio"])
                columna["duracion_minutos"] = float(columna["duracion_minutos"])
                columna["intentos_fallidos"] = int(columna["intentos_fallidos"])
                columna["reportes_trampa"] = int(columna["reportes_trampa"])
            return list(ruta_archivo)



cargar_telemetria("C:\\Users\\UNAHUR\\Desktop\\TP\\gamesec_logs.csv")