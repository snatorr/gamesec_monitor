from carga import cargar_telemetria


def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    total = len(sesiones)
    suma_ping = 0
    suma_duracion = 0.0
    suma_competitivas = 0

    for sesion in sesiones:
        suma_ping += sesion["ping_promedio"]
        suma_duracion += sesion["duracion_minutos"]
        if sesion["tipo_partida"] in ("Competitiva", "Torneo"):
            suma_competitivas += 1

    return {
        "total_sesiones" : total,
        "ping_promedio" : round(suma_ping / total, 2),
        "duracion_promedio" : round(suma_duracion / total, 2),
        "porcentaje_competitivas" : round(suma_competitivas / total * 100, 2),
    }

def analizar_por_servidor(sesiones: list[dict]) -> dict:

    diccionario_acumulador = {}

    for sesion in sesiones:
        servidor = sesion["servidor"]

        if servidor not in diccionario_acumulador:
            diccionario_acumulador[servidor] = {"cantidad" : 0, "suma_ping" : 0, "suma_fps" : 0}

        diccionario_acumulador[servidor]["cantidad"] += 1
        diccionario_acumulador[servidor]["suma_ping"] += sesion["ping_promedio"]
        diccionario_acumulador[servidor]["suma_fps"] += sesion["fps_promedio"]

    resultado = {}

    for nombre, datos in diccionario_acumulador.items():
        resultado[nombre] = {
            "cantidad" : datos["cantidad"],
            "ping_promedio" : round(datos["suma_ping"] / datos["cantidad"], 2),
            "fps_promedio" : round(datos["suma_fps"] / datos["cantidad"], 2),
        }

    return resultado


resultados = analizar_por_servidor(cargar_telemetria("src/gamesec_logs.csv"))


print(resultados)