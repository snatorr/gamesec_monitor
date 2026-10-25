import csv
import os



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

        for fila in lector:

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