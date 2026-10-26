from carga import cargar_telemetria

#Yo pondria esto para facilitarnos la ruta
sesiones= cargar_telemetria("gamesec_logs.csv")


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

    """Aqui cambie el IF__ NOT IN, por el .get() ya que tambien es una herramienta de diccionario acumulador.
    Su ventaja en ese caso seria que si una clave no existe, devolvera el argumento que le demos, que seria 0 

    Esto acorde a la consigna: " el diccionario debe poblarse dinámicamente a medida que aparecen servidores nuevos en el archivo." 
    """
    
    diccionario_acumulador = {}

    for sesion in sesiones:
        servidor_actual= sesion["servidor"]
        datos_del_servidor= diccionario_acumulador.get(region_actual,{"cantidad": 0, 
                                                               "ping_promedio": 0, 
                                                               "fps_promedio": 0})
        datos_del_servidor["cantidad"]+=1
        datos_del_servidor["ping_promedio"]+=(sesion["ping_promedio"])
        datos_del_servidor["fps_promedio"]+=(sesion["fps_promedio"])
    
        diccionario_acumulador[servidor_actual]=datos_del_servidor
    
    for key, value in diccionario_acumulador.items():
        
        value["ping_promedio"]= round(value["ping_promedio"]/value["cantidad"],1)
        value["fps_promedio"]= round(value["fps_promedio"]/value["cantidad"],1)
    
    return diccionario_acumulador


resultados = analizar_por_servidor(sesiones)


print(resultados)
