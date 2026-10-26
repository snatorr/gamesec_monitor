from carga import cargar_telemetria
from procesamiento import calcular_estadisticas_globales, analizar_por_servidor,clasificar_incidentes,exportar_reporte

sesiones = []

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
                estadisticas = clasificar_incidentes(sesiones)
                print(estadisticas)
            elif opcion == "5":
                exportar_reporte(sesiones, ruta_salida='reporte_gamesec.txt') 
                print("reportes exportados exitosamente")
    elif opcion == "6":
        print("Saliendo del programa...")
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")
