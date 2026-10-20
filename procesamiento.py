import csv




def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    with open(sesiones, "r", newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter=",")
        sesiones_registradas = {
            "total_Sesiones": [],
            "ping_promedio": [],
            "duracion_promedio": [],
            "porcentaje_competitivas": [],
        }


        for columna in lector:
            columna["id_sesion"].join((sesiones_registradas["total_Sesiones"]))
    print(sesiones_registradas)




calcular_estadisticas_globales("C:\\Users\\UNAHUR\\Desktop\\TP\\gamesec_logs.csv")

