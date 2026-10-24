import csv
import os

from procesamiento import calcular_estadisticas_globales


def cargar_telemetria(ruta_archivo: str) -> list[dict]:

    """
    Lee el archivo .CSV y retorna una lista de diccionarios con los type casteados
    Utilizamos FileNotFoundError para verificar que el archivo se encuentre en el directorio
    y ValueError por si está vacío.
    """

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no pudo ser encontrado.")
    
    sesiones = []

    with open(ruta_archivo, "r", newline="", encoding="utf-8") as f:

        lector = csv.DictReader(f, delimiter=",")

        for numero_fila, fila in enumerate(lector, start=2):
            fila["id_sesion"] = int(fila["id_sesion"])
            fila["ping_promedio"] = int(fila["ping_promedio"])
            fila["fps_promedio"] = int(fila["fps_promedio"])
            fila["duracion_minutos"] = float(fila["duracion_minutos"])
            fila["intentos_fallidos"] = int(fila["intentos_fallidos"])
            fila["reportes_trampa"] = int(fila["reportes_trampa"])
            sesiones.append(fila) 

    if len(sesiones) == 0:
        raise ValueError("El archivo no tiene registros")
    
    return sesiones

sesiones = []
with open('gamesec_logs.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        # Convertimos a número las columnas que lo necesiten, por ejemplo:
        fila['ping_promedio'] = float(fila['ping_promedio']) if fila['ping_promedio'] != '' else None
        fila['fps_promedio'] = float(fila['fps_promedio']) if fila['fps_promedio'] != '' else None
        sesiones.append(fila)
from procesamiento import analizar_por_servidor

datos_cargados = cargar_telemetria("gamesec_logs.csv")
resultado = calcular_estadisticas_globales(datos_cargados)
resultado_servidores = analizar_por_servidor(sesiones)
print(resultado_servidores)