carga import cargar_telemetria
from procesamiento import calcular_estadisticas_globales, analizar_por_servidor,clasificar_incidentes

sesiones = []

def exportar_reporte(sesiones: list[dict], ruta_salida: str = "reporte_gamesec.txt"):

    """Consolida las estadísticas globales, el rendimiento regional y
    la auditoría de incidentes respetando la estructura modelo exacta.
    """

    estadisticas_globales = calcular_estadisticas_globales(sesiones)
    por_servidor = analizar_por_servidor(sesiones)
    distribucion_estados, lista_criticos = clasificar_incidentes(sesiones)
    
    total_sesiones = estadisticas_globales.get('total_sesiones', len(sesiones))
    
    normales_cant = distribucion_estados.get('Normal', 0)
    sospechosos_cant = distribucion_estados.get('Sospechosos', 0)
    criticos_cant = distribucion_estados.get('Crítico', 0)
    
    pct_normales = (normales_cant / total_sesiones * 100) if total_sesiones > 0 else 0
    pct_sospechosos = (sospechosos_cant / total_sesiones * 100) if total_sesiones > 0 else 0
    pct_criticos = (criticos_cant / total_sesiones * 100) if total_sesiones > 0 else 0

    import datetime
    fecha_hoy = datetime.date.today().strftime("%d/%m/%Y")

    with open(ruta_salida, "w", encoding="utf-8") as f:
        # Encabezado principal

        f.write("=" * 70 + "\n")
        f.write("             REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC              \n")
        f.write("=" * 70 + "\n")
        f.write(f"Fecha de generación: {fecha_hoy}\n\n")
        
        # [1] Resumen global operativo
        """"" es posible usar "writelines, aun deberia usarse el \ n al final pero 
        ayuda a simplificar el codigo. Tambien el .get() es inecesario ya que por ej "ping_promedio"
        siempre esta en los diccionarios, si un diccionario no incluye esa clave igual daria error."""

        """ Un error a chequear en todo el menu es que se usa : 'cantidad' y no "cantidad". Las comillas unicas
         son algo que devuelve la IA  """

        """ cambie el nombre de "globales" a "estadisticas_globales. Creo que algunos nombres podrian ser mas claros
         y no solo intentar que sean resumidos. """

        f.writelines([
            "[1] RESUMEN GLOBAL OPERATIVO\n",
            "-" * 70 + "\n",
            f"Total de sesiones procesadas: {total_sesiones}\n",
            f"Ping promedio global: {estadisticas_globales["ping_promedio"]:.2f} ms\n",
            f"Duración media de partida: {estadisticas_globales["duracion_promedio"]:.2f} min\n",
            f"Partidas de alta competencia (Ranked/Torneo): {estadisticas_globales["porcentaje_competitivas"]:.2f}%\n\n",
        ])
        
        # [2] Rendimiento regional por servidor
        f.write("[2] RENDIMIENTO REGIONAL POR SERVIDOR\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Servidor':<18} | {'Sesiones':<8} | {'Ping Promedio':<13} | {'FPS Promedio'}\n")
        f.write("-" * 70 + "\n")
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

        """" Esta consigna obligatoriamente debe ser una conclusion nuestra, yo coloque los datos de la primera. """
        
        # [4] Conclusiones técnicas del equipo
        f.write("[4] CONCLUSIONES TÉCNICAS DEL EQUIPO\n")
        f.write("-" * 70 + "\n")
        f.write("SA-BuenosAires registra la mayor proporción de incidentes críticos, aunque la diferencia con SA-SaoPaulo es pequeña.\n")
        f.write("2. La tasa de incidentes críticos representa un porcentaje menor al 7% del total, evidenciando un comportamiento general estable de la base de usuarios.\n")
        f.write("3. El rendimiento de cuadros por segundo (FPS) se mantiene sumamente competitivo y estable por encima de los 80 FPS promedio en todas las ubicaciones geográficas.\n\n")
        
        # Pie de página
        f.write("=" * 70 + "\n")
        f.write("                             FIN DEL REPORTE GAMESEC                  \n")
        f.write("=" * 70 + "\n")
        
    print(f"📁 ¡Reporte estructurado guardado correctamente en: {ruta_salida}!")


while True:
    print("1) Cargar y validar dataset")
    print("2) Ver estadísticas globales de servidores")
    print("3) Ver rendimiento por región de servidor")
    print("4) Auditar incidentes de seguridad (Críticos y Sospechosos)")
    print("5) Exportar reporte consolidado (reporte_gamesec.txt)")
    print("6) Salir")

    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        sesiones = cargar_telemetria("gamesec_logs.csv")
    elif opcion in ("2", "3", "4", "5"):
        if len(sesiones) == 0:
            print("primero carga el dataset")
        else:
            if opcion == "2":
                estadisticas = calcular_estadisticas_globales(sesiones)
                print(estadisticas)
            elif opcion == "3":
                estadisticas = analizar_por_servidor(sesiones)
                print(estadisticas)
            elif opcion == "4":
                distribucion_estados, lista_criticos = clasificar_incidentes(sesiones)
                print("Distribución de estados:", distribucion_estados)
                print("Sesiones críticas:", lista_criticos)
            elif opcion == "5":
                exportar_reporte(sesiones, ruta_salida='reporte_gamesec.txt') 
                print("reportes exportados exitosamente")
    elif opcion == "6":
        print("Saliendo del programa...")
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")

