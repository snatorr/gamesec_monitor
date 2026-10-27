import os
from datetime import datetime
from src.carga import cargar_telemetria
from src.procesamiento import (calcular_estadisticas_globales, analizar_por_servidor, clasificar_incidentes)

"""
Para realizar el menú, utilizamos la función .write() e importamos todos los módulos
anteriormente creados.

Este módulo es capáz de recibir el archivo "gamesec_logs.csv" y leerlo desde cualquier
sistema operatívo gracias a la libreria os y su función os.path.join
"""


carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(carpeta_actual, "gamesec_logs.csv")

def mostrar_menu():
    print("=" * 41)
    print("   GAMESEC MONITOR — PANEL DE CONTROL")
    print("=" * 41)
    print("1. Cargar y validar dataset")
    print("2. Ver estadísticas globales de servidores")
    print("3. Ver rendimiento por región de servidor")
    print("4. Auditar incidentes de seguridad (Críticos y Sospechosos)")
    print("5. Exportar reporte consolidado (reporte_gamesec.txt)")
    print("6. Salir")
    print("=" * 41)

def mostrar_estadisticas(sesiones: list[dict]):
    estadisticas = calcular_estadisticas_globales(sesiones)
    print("\n            RESUMEN GLOBAL")
    print("—" * 41)
    print(f"Total de sesiones procesadas: {estadisticas["total_sesiones"]}")
    print(f"Ping promedio global: {estadisticas["ping_promedio"]} ms")
    print(f"Duración media de partida: {estadisticas["duracion_promedio"]} min")
    print(f"Partidas de alta competencia (Ranked/Torneo): {estadisticas["porcentaje_competitivas"]}%\n")

def mostrar_por_servidor(sesiones: list[dict]):
    datos = analizar_por_servidor(sesiones)
    print("\n           RENDIMIENTO POR SERVIDOR")
    print("-" * 48)
    print("Servidor  |  Sesiones  |  Ping Promedio | FPS Promedio")
    print("-" * 48)
    for nombre, ficha in datos.items():
        print(f"{nombre} | {ficha["cantidad"]} sesiones | {ficha["ping_promedio"]} ms | {ficha["fps_promedio"]} fps")
    print()

def mostrar_auditoria(sesiones: list[dict]):
    resumen, criticos = clasificar_incidentes(sesiones)
    print("\n   AUDITORIA DE SEGURIDAD E INCIDENTES")
    print("-" * 41)
    print("Distribución de estados de seguridad:")
    print("-" * 41)
    print(f"Normales: {resumen["Normal"]}")
    print(f"Sospechosos: {resumen["Sospechoso"]}")
    print(f"CRIticos: {resumen["Crítico"]}")
    print("-" * 41)
    print()

    print("-" * 41)
    print("Detalle de Sesiones Críticas Detectadas:")
    print("-" * 41)
    for sesion in criticos:
        print(f"[!] Sesión {sesion["id_sesion"]} | {sesion["jugador_id"]} | {sesion["servidor"]}")
        print(f"     Motivo: {sesion["motivo"]}")
    print()

def exportar_reporte(sesiones: list[dict], ruta_salida: str = "reporte_gamesec.txt"):
    estadisticas = calcular_estadisticas_globales(sesiones)
    analizar = analizar_por_servidor(sesiones)
    resumen, criticos = clasificar_incidentes(sesiones)
    total = estadisticas["total_sesiones"]

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("            REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC\n")
        f.write("=" * 70 + "\n")
        f.write(f"Fecha de generación: {datetime.now().strftime("%d/%m/%Y")}" + "\n\n")

        f.write("[1] RESUMEN GLOBAL OPERATIVO\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total de sesiones procesadas: {total}\n")
        f.write(f"Ping promedio global: {estadisticas["ping_promedio"]} ms\n")
        f.write(f"Duración media de partida: {estadisticas["duracion_promedio"]} min\n")
        f.write(f"Partidas de alta competencia (RANKED/TORNEO): {estadisticas["porcentaje_competitivas"]}%\n\n")

        f.write("[2] RENNDIMIENTO REGIONAL POR SERVIDOR\n")
        f.write("-" * 70 + "\n")
        f.write("Servidor | Sesiones | Ping Promedio | FPS Promedio\n")
        for nombre, ficha in analizar.items():
            f.write(f"{nombre} | {ficha["cantidad"]} | {ficha["ping_promedio"]} ms | {ficha["fps_promedio"]} fps\n")

        f.write("\n[3] AUDITORIA DE SEGURIDAD E INCIDENTES\n")
        f.write("-" * 70 + "\n")
        f.write("Distribución de estados de seguridad:\n")
        for estado in ("Normal", "Sospechoso", "Crítico"):
            porcentaje = round(resumen[estado] / total * 100, 2)
            f.write(f" – {estado} : {resumen[estado]} sesiones ({porcentaje}%)\n")

        f.write("\nDetalle de Sesiones Críticas Detectadas:\n")
        for critico in criticos:
            f.write(f" [!] Sesión #{critico["id_sesion"]} | Jugador: {critico["jugador_id"]} | Servidor {critico["servidor"]}\n")
            f.write(f"       Motivo: {critico["motivo"]}\n")

        f.write("\n[4] CONCLUSIONES TECNICAS DEL GRUPO\n")
        f.write("-" * 70 + "\n")
        f.write("SA-BuenosAires registra la mayor proporción de incidentes críticos, aunque la diferencia con SA-SaoPaulo es pequeña.\n")
        f.write("todo sigue estable no hay muchos incidentes espero que siga igual\n")
        f.write("DYLAN, BREN, ESCRIBIR CONCLUSIONES ACÁ\n")

        f.write("-" * 70 + "\n")
        f.write("                  Fin del reporte GAMESEC MONITOR\n")
        f.write("-" * 70 + "\n")
    print(f"\nReporte exportado con éxito en: {ruta_salida}\n")

def main():
    sesiones = []
    while True:
        mostrar_menu()
        opcion = int(input("Seleccione una opción: ").strip())

        if opcion == 1:
            try:
                sesiones = cargar_telemetria(ruta_archivo)
                print(f"\nDataset cargado: {len(sesiones)} sesiones válidas.\n")
            except (ValueError, FileNotFoundError) as error:
                print(f"\nNo se pudo cargar el archivo: {error}\n")
        elif opcion in (2, 3, 4, 5):
            if not sesiones:
                print("\nPrimero debe ser cargado el dataset (OPCIÓN 1). \n")
            elif opcion == 2:
                mostrar_estadisticas(sesiones)
            elif opcion == 3:
                mostrar_por_servidor(sesiones)
            elif opcion == 4:
                mostrar_auditoria(sesiones)
            elif opcion == 5:
                exportar_reporte(sesiones)



        if opcion == 6:
            print("Hasta luego.")
            break

if __name__ == "__main__":
    main()
