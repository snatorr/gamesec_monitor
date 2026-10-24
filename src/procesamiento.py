
from carga import cargar_telemetria

sesiones= cargar_telemetria("gamesec_logs.csv")

def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
  sesiones_registradas = {
      "total_Sesiones": [len(sesiones)],
      "ping_promedio": [obtener_promedio(sesiones,"ping_promedio") ],
      "duracion_promedio": [obtener_promedio(sesiones,"duracion_minutos")],
      "porcentaje_competitivas": [],
  }
  print(sesiones_registradas)

#Hice una funcion general para calcular el promedio pero tambien se puede resolver dentro del mismo value demanera mas corta asi:
#round( sum( [sesion[columna] for sesion in sesiones] ) / len(sesiones), 2 


def obtener_promedio(sesiones,columna):
  suma=0
  for sesion in sesiones:
    suma+= sesion[columna]
  return round( suma/ len(sesiones) ,2)

print(calcular_estadisticas_globales(sesiones))
