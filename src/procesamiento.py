
def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    total_sesiones = len(sesiones)
    contador_competitivas = 0.0
    suma_ping = 0.0
    suma_duracion = 0.0

    for sesion in sesiones:
        if sesion["tipo_partida"] in ("Competitiva", "Torneo"):
            contador_competitivas += 1
        if sesion["ping_promedio"] is not None:
            suma_ping += sesion["ping_promedio"]
        if sesion["duracion_minutos"] is not None:
            suma_duracion += sesion["duracion_minutos"]
        if total_sesiones == 0:
            return {
                "total_sesiones": 0,
                "ping_promedio": 0.0,
                "duracion_promedio": 0.0,
                "porcentaje_competitivas": 0.0
            }
     
    return {
        "total_sesiones": total_sesiones,
        "porcentaje_competitivas": round(contador_competitivas / total_sesiones * 100, 2),
        "ping_promedio": round(suma_ping / total_sesiones, 2),
        "duracion_promedio": round(suma_duracion / total_sesiones, 2),
    }
def analizar_por_servidor(sesiones: list[dict]) -> dict:
    por_servidores = {}
    ping_promedios = 0.0
    fps_promedios = 0.0
    resultado = {}

    for sesion in sesiones:
        servidor = sesion["servidor"]
        if servidor not in por_servidores:
            por_servidores[servidor] = {
                "cantidad": 0,
                "ping_promedio": 0.0,
                "fps_promedio": 0.0
            }
        if sesion["ping_promedio"] is not None:
            por_servidores[servidor]["ping_promedio"] += sesion["ping_promedio"]
        if sesion["fps_promedio"] is not None:
            por_servidores[servidor]["fps_promedio"] += sesion["fps_promedio"]
        por_servidores[servidor]["cantidad"] += 1
    for servidor, datos in por_servidores.items():
        cantidad = datos["cantidad"]
        resultado[servidor] = {
            "cantidad": cantidad,
            "ping_promedio": round(datos["ping_promedio"] / cantidad, 2),
            "fps_promedio": round(datos["fps_promedio"] / cantidad, 2) ,
        }
    return resultado