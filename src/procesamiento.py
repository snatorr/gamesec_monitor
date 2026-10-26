from carga import cargar_telemetria

#Yo pondria esto para facilitarnos la ruta
sesiones= cargar_telemetria("gamesec_logs.csv")

###
""" Consigna 2: Módulo procesamiento.py — Métricas Globales de Operación """
###
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
    
###
""" Consigna 3: Módulo procesamiento.py — Agrupamiento por Región de Servidor """
###

def analizar_por_servidor(sesiones: list[dict]) -> dict:

    """Aqui cambie el IF__ NOT IN, por el .get() ya que tambien es una herramienta de diccionario acumulador.
    Su ventaja en ese caso seria que si una clave no existe, devolvera el argumento que le demos, que seria 0 

    Esto acorde a la consigna: " el diccionario debe poblarse dinámicamente a medida que aparecen servidores nuevos en el archivo." 
    """
    
    diccionario_acumulador = {}

    for sesion in sesiones:
        servidor_actual= sesion["servidor"]
        datos_del_servidor= diccionario_acumulador.get(servidor_actual,{"cantidad": 0, 
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

###
""" Consigna 4: Módulo procesamiento.py — Motor de Clasificación de Incidentes """
###

def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    # Retorna una tupla:
    # 1. Diccionario resumen de frecuencias: {"Normal": N, "Sospechoso": S, "Crítico": C}
    # 2. Lista de diccionarios simplificados correspondientes únicamente a los eventos 'Crítico'

#1. CRÍTICO: Si la sesión registra (reportes_trampa >= 3) O BIEN (intentos_fallidos >= 4).
#2. SOSPECHOSO: Si no es Crítico y cumple: [(ping_promedio > 200 Y intentos_fallidos >= 2) O (reportes_trampa == 2)].
#3. NORMAL: Cualquier sesión que no encaje en las categorías anteriores.
#{
#    "id_sesion": 14,
#    "jugador_id": "User_482",
#    "servidor": "NA-Virginia",
#    "motivo": "Exceso de reportes por trampa (4) e intentos fallidos (5)"
#}
  eventos_criticos=[]
  resumen_de_frecuencias={"Normal":0,
                          "Sospechoso":0,
                          "Crítico":0}

  for sesion in sesiones:
      
    if sesion["reportes_trampa"]>3 or sesion["intentos_fallidos"]>=4:
      resumen_de_frecuencias["Crítico"]+=1
      mensaje_critico= f"Exceso de reportes ({sesion["reportes_trampa"]}) e intentos fallidos ({sesion["intentos_fallidos"]})"
      diccionario_simplificado={"id_sesion":sesion["id_sesion"],
                                "jugador_id": sesion["jugador_id"],
                                "servidor":sesion["servidor"],
                                "motivo":mensaje_critico}
      eventos_criticos.append(diccionario_simplificado)
    elif (sesion["ping_promedio"]>200 and sesion["intentos_fallidos"]>=2) or sesion["reportes_trampa"]==2:
      resumen_de_frecuencias["Sospechoso"]+=1
    else:
      resumen_de_frecuencias["Normal"]+=1

  clasificacion_de_incidentes= (resumen_de_frecuencias,eventos_criticos)


  return clasificacion_de_incidentes




resultados = clasificar_incidentes(sesiones)


print(resultados)

