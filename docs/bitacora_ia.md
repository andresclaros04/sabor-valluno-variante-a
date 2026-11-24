# Bitácora de uso de IA

Todo uso de IA relacionado con el proyecto debe registrarse, incluso cuando solo se consulte un concepto.

## Registro 1

- Fecha: 23/11/2026
- Herramienta: ChatGPT Codex
- Tipo de uso: interpretación de consigna y planificación
- Consulta textual: solicitud de acompañamiento desde la semana posterior al modelado hasta terminar el proyecto
- Qué se aceptó: estructura semanal, lista de entregables y organización inicial de carpetas
- Qué se modificó y por qué: no se generó código porque todavía faltan la variante y el diagrama v1
- Archivo o clase: `PLAN_PROYECTO.md`, `docs/acta_consultas.md`, `docs/bitacora_ia.md`
- ¿Lo explico sin ayuda?: pendiente de completar por el estudiante

## Plantilla para los siguientes usos

- Fecha:
- Herramienta:
- Tipo de uso:
- Consulta textual:
- Qué se aceptó:
- Qué se modificó y por qué:
- Archivo o clase:
- ¿Lo explico sin ayuda?:

## Registro 2

- Fecha: 23/11/2026
- Herramienta: ChatGPT Codex
- Tipo de uso: revisión de diagrama
- Consulta textual: envío de fotografía del diagrama v1 realizado en aula
- Qué se aceptó: conservar el diagrama original y documentar las correcciones para el v2
- Qué se modificó y por qué: se propuso mover la cantidad a `PedidoProducto`, hacer que `Combo` herede de `Producto` y renombrar las clases según la consigna
- Archivo o clase: `docs/diagrama_v1.jpg`, `docs/revision_diagrama_v1.md`
- ¿Lo explico sin ayuda?: pendiente de completar por el estudiante

## Registro 3

- Fecha: 23/11/2026
- Herramienta: ChatGPT Codex
- Tipo de uso: generación y revisión de código
- Consulta textual: confirmación de la variante A y solicitud de continuar el proyecto
- Qué se aceptó: jerarquías de productos, pedidos y pagos; clase gestora; pruebas y menú de consola
- Qué se modificó y por qué: se eliminó la comprobación por tipo dentro de `Combo` para usar polimorfismo; posteriormente se retiró la regla de retraso porque el docente decidió no evaluarla
- Archivo o clase: `modelo/`, `restaurante.py`, `main.py`, `pruebas.py`
- ¿Lo explico sin ayuda?: pendiente de completar por el estudiante

## Registro 4

- Fecha: 23/11/2026
- Herramienta: ChatGPT Codex
- Tipo de uso: generación y prueba de funcionalidad opcional
- Consulta textual: continuar completando el proyecto mientras se confirmaba el alcance de la regla de retraso
- Qué se aceptó: guardado y carga de datos mediante JSON
- Qué se modificó y por qué: se añadió `persistencia.py` separado para no mezclar serialización con los cálculos del modelo
- Archivo o clase: `persistencia.py`, `main.py`, `pruebas.py`
- ¿Lo explico sin ayuda?: pendiente de completar por el estudiante

## Registro 5

- Fecha: 23/11/2026
- Herramienta: ChatGPT Codex
- Tipo de uso: revisión y corrección del diagrama de clases v2
- Consulta textual: "entonces hagamos las correcciones mas importante, empezando por el que tiene que ver con el diagrama que es el pilar de este proyecto y ademas recuerdo que el docente repitio emcarecidamente que el codigo debe estar deacuerdo a los diagrmas"
- Qué se aceptó: completar el diagrama v2 para que represente fielmente el código actual y las exigencias del documento del docente
- Qué se modificó y por qué: se agregaron atributos, propiedades, constructores, métodos, tipos, visibilidad, relaciones, multiplicidades y doce notas de cambios respecto al v1. También se verificó automáticamente que las 15 clases y sus 126 métodos aparezcan en el archivo Mermaid. No se modificó el código del modelo en esta etapa.
- Archivo o clase: `docs/diagrama_v2.mmd`, `docs/diagrama_v2.png`
- ¿Lo explico sin ayuda?: pendiente de completar por el estudiante

## Registro 6

- Fecha: 23/11/2026
- Herramienta: ChatGPT Codex
- Tipo de uso: revisión visual con fotografía del diagrama v1 aprobado
- Consulta textual: "ese el diagrama que fue sellado por el docente"
- Qué se aceptó: utilizar la fotografía sellada como línea base oficial y mantener en el v2 la misma distribución visual de productos, pedidos, pagos, cliente y clases hijas
- Qué se modificó y por qué: se reemplazó `docs/diagrama_v1.png` por la fotografía aprobada; el v2 se reorganizó para seguir el formato del papel, se conservaron las cajas y flechas de herencia y se añadió un reporte detallado que justifica cada diferencia. El código no se modificó.
- Archivo o clase: `docs/diagrama_v1.png`, `docs/diagrama_v2.png`, `docs/diagrama_v2.mmd`, `docs/cambios_v1_v2.md`, `docs/revision_diagrama_v1.md`
- ¿Lo explico sin ayuda?: pendiente de completar por el estudiante

