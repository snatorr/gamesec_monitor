# GameSec Monitor

**Trabajo Práctico Integrador - Taller de Programación I (2C 2026)**
Universidad Nacional de Hurlingham - Instituto de Tecnología e Ingeniería

Herramienta de consola en Python que procesa la telemetría de servidores de videojuegos (`gamesec_logs.csv`), calcula métricas operativas y clasifica las sesiones como Normal, Sospechosa o Crítica mediante reglas heurísticas.

## Integrantes

| Nombre y apellido | DNI | Carrera |
|---|---|---|
| Dylan Correa Diaz | 48055943 | Programación de Videojuegos |
| Brenda Carrizo | 42886034 | Programación de Videojuegos |
| Santiago Barraza Narbaez | 46417605 | Licenciatura en Ciberseguridad |

## Requisitos

- Python 3.10 o superior.
- Solo librerías estándar (`csv`, `os`, `datetime`). No se usa Pandas ni NumPy.

## Cómo ejecutar

Desde la carpeta del proyecto:

```
python main.py
```

Primero elegir la opción **1** (cargar y validar el dataset); luego se pueden usar las demás opciones del menú.

## Estructura del proyecto

```
gamesec_monitor/
├── main.py              # Menú interactivo y exportación del reporte
├── gamesec_logs.csv     # Dataset provisto por la cátedra (150 sesiones)
├── reporte_gamesec.txt  # Reporte generado con la opción 5
├── README.md
└── src/
    ├── carga.py            # Lectura, tipado y validación del CSV
    └── procesamiento.py    # Estadísticas, agrupamiento por servidor y clasificación de incidentes
```

## Menú

1. Cargar y validar dataset
2. Ver estadísticas globales de servidores
3. Ver rendimiento por región de servidor
4. Auditar incidentes de seguridad
5. Exportar reporte consolidado (`reporte_gamesec.txt`)
6. Salir

## Reglas de clasificación de incidentes

- **Crítico:** `reportes_trampa >= 3` o `intentos_fallidos >= 4`.
- **Sospechoso:** si no es crítico y cumple `(ping_promedio > 200 y intentos_fallidos >= 2)` o `reportes_trampa == 2`.
- **Normal:** cualquier otra sesión.
