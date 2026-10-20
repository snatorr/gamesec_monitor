import csv


def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    with open(sesiones, "r", newline="", encoding="utf-8") as f:
        sesiones_registradas = {
            "total_Sesiones": [],
            "ping_promedio": [],
        }
        sesiones_registradas["total_Sesiones"].append(len(sesiones))
        print(sesiones_registradas)

calcular_estadisticas_globales("procesamientos/gamesec_logs.csv")