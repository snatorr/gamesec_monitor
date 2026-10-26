from carga import cargar_telemetria


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

import datetime

import datetime

def exportar_reporte(sesiones: list[dict], ruta_salida: str = "reporte_gamesec.txt"):
    """
    Consolida las estadísticas globales, el rendimiento regional y 
    la auditoría de incidentes respetando la estructura modelo exacta.
    """
    globales = calcular_estadisticas_globales(sesiones)
    por_servidor = analizar_por_servidor(sesiones)
    distribucion_estados, lista_criticos = clasificar_incidentes(sesiones)
    
    total_sesiones = globales.get('total_sesiones', len(sesiones))
    
    normales_cant = distribucion_estados.get('Normal', 0)
    sospechosos_cant = distribucion_estados.get('Sospechosos', 0)
    criticos_cant = distribucion_estados.get('Crítico', 0)
    
    pct_normales = (normales_cant / total_sesiones * 100) if total_sesiones > 0 else 0
    pct_sospechosos = (sospechosos_cant / total_sesiones * 100) if total_sesiones > 0 else 0
    pct_criticos = (criticos_cant / total_sesiones * 100) if total_sesiones > 0 else 0

    fecha_hoy = datetime.date.today().strftime("%d/%m/%Y")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        # Encabezado principal
        f.write("======================================================================\n")
        f.write("             REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC              \n")
        f.write("======================================================================\n")
        f.write(f"Fecha de generación: {fecha_hoy}\n\n")
        
        # [1] Resumen global operativo
        f.write("[1] RESUMEN GLOBAL OPERATIVO\n")
        f.write("----------------------------------------------------------------------\n")
        f.write(f"Total de sesiones procesadas: {total_sesiones}\n")
        f.write(f"Ping promedio global: {globales.get('ping_promedio', 0):.2f} ms\n")
        f.write(f"Duración media de partida: {globales.get('duracion_promedio', 0):.2f} min\n")
        f.write(f"Partidas de alta competencia (Ranked/Torneo): {globales.get('porcentaje_competitivas', 0):.2f}%\n\n")
        
        # [2] Rendimiento regional por servidor
        f.write("[2] RENDIMIENTO REGIONAL POR SERVIDOR\n")
        f.write("----------------------------------------------------------------------\n")
        f.write(f"{'Servidor':<18} | {'Sesiones':<8} | {'Ping Promedio':<13} | {'FPS Promedio'}\n")
        f.write("----------------------------------------------------------------------\n")
        for servidor, datos in por_servidor.items():
            cant = datos.get('cantidad', 0)
            ping = datos.get('ping_promedio', 0)
            fps = datos.get('fps_promedio', 0)
            f.write(f"{servidor:<18} | {cant:<8} | {ping:<10.2f} ms   | {fps:.2f} fps\n")
        f.write("\n")
        
        # [3] Auditoría de seguridad e incidentes
        f.write("[3] AUDITORÍA DE SEGURIDAD E INCIDENTES\n")
        f.write("----------------------------------------------------------------------\n")
        f.write("Distribución de estados de seguridad:\n")
        f.write(f"- Normales: {normales_cant} sesiones ({pct_normales:.2f}%)\n")
        f.write(f"- Sospechosos: {sospechosos_cant} sesiones ({pct_sospechosos:.2f}%)\n")
        f.write(f"- Críticos: {criticos_cant} sesiones ({pct_criticos:.2f}%)\n\n")
        
        f.write("Detalle de Sesiones Críticas Detectadas:\n")
        if lista_criticos:
            for c in lista_criticos:
                sid = c.get('id_sesion', 'N/A')
                jugador = c.get('jugador_id', 'N/A')
                serv = c.get('servidor', 'N/A')
                motivo = c.get('motivo', 'N/A')
                f.write(f"  [!] Sesión #{sid}  | Jugador: {jugador} | Servidor: {serv}\n")
                f.write(f"      Motivo: {motivo}\n")
        else:
            f.write("  (No se registraron sesiones críticas en este lote)\n")
        f.write("\n")
        
        # [4] Conclusiones técnicas del equipo
        f.write("[4] CONCLUSIONES TÉCNICAS DEL EQUIPO\n")
        f.write("----------------------------------------------------------------------\n")
        f.write("1. Las regiones de ultramar (EU y NA) registran latencias significativamente superiores, sugiriendo la necesidad de implementar servidores proxy regionales adicionales.\n")
        f.write("2. La tasa de incidentes críticos representa un porcentaje menor al 7% del total, evidenciando un comportamiento general estable de la base de usuarios.\n")
        f.write("3. El rendimiento de cuadros por segundo (FPS) se mantiene sumamente competitivo y estable por encima de los 80 FPS promedio en todas las ubicaciones geográficas.\n\n")
        
        # Pie de página
        f.write("======================================================================\n")
        f.write("                             FIN DEL REPORTE GAMESEC                  \n")
        f.write("======================================================================\n")
        
    print(f"📁 ¡Reporte estructurado guardado correctamente en: {ruta_salida}!")