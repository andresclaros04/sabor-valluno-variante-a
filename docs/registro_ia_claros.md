# Registro personal de uso de IA

- Estudiante: Andrés Claros
- Variante: A
- Proyecto: Sistema de Pedidos Sabor Valluno

| N.º | Fecha | Herramienta | Tipo de uso | Consulta | Qué acepté | Qué modifiqué y por qué | Archivo o clase | ¿Lo explico sin ayuda? |
|---:|---|---|---|---|---|---|---|---|
| 1 | 23/11/2026 | ChatGPT Codex | Concepto y planificación | Interpretar entregas y organizar el trabajo desde la semana 2 | Estructura semanal y entregables | Se dejó el código pendiente hasta conocer la variante | `PLAN_PROYECTO.md` | Pendiente |
| 2 | 23/11/2026 | ChatGPT Codex | Revisión | Revisar la fotografía del diagrama v1 | Lista de cambios para el v2 | Se conservó el v1 original y se documentaron las diferencias | `docs/revision_diagrama_v1.md` | Pendiente |
| 3 | 23/11/2026 | ChatGPT Codex | Generación y revisión de código | Implementar la variante A según la consigna | Jerarquías, validaciones, menú, pruebas y documentación | Se eliminó la comprobación por tipo en `Combo`; la regla de retraso se retiró después de que el docente decidió no evaluarla | `modelo/`, `restaurante.py`, `main.py`, `pruebas.py` | Pendiente |
| 4 | 23/11/2026 | ChatGPT Codex | Funcionalidad opcional | Completar persistencia y pruebas | Persistencia JSON | Se separó la serialización en `persistencia.py` para no mezclarla con el modelo | `persistencia.py`, `main.py`, `pruebas.py` | Pendiente |
| 5 | 23/11/2026 | ChatGPT Codex | Revisión y corrección del diagrama | "entonces hagamos las correcciones mas importante, empezando por el que tiene que ver con el diagrama que es el pilar de este proyecto y ademas recuerdo que el docente repitio emcarecidamente que el codigo debe estar deacuerdo a los diagrmas" | Diagrama v2 completo y auditoría automática de correspondencia | Se añadieron los atributos, propiedades, constructores, métodos, tipos, visibilidad, relaciones, multiplicidades y las doce notas de cambio que faltaban; el código del modelo no se modificó | `docs/diagrama_v2.mmd`, `docs/diagrama_v2.png` | Pendiente |
| 6 | 23/11/2026 | ChatGPT Codex | Revisión visual con evidencia aprobada | "ese el diagrama que fue sellado por el docente" | Usar la fotografía sellada como línea base visual y lógica | Se reemplazó la evidencia v1 por la fotografía aprobada, se reorganizó el v2 con la misma distribución del papel y se amplió el reporte de cambios; no se modificó el código | `docs/diagrama_v1.png`, `docs/diagrama_v2.png`, `docs/diagrama_v2.mmd`, `docs/cambios_v1_v2.md`, `docs/revision_diagrama_v1.md` | Pendiente |
| 7 | 24/11/2026 | ChatGPT Codex | Replanteamiento con cambios mínimos | "sobre los diagrmas que esta ahi, necesito que no se cambie demasiado porque el docente no permite rehacer o hacer grandes cambios en el diagrama y que solo me limite a cambiar atributos o metodos en lo posible" | Preparar una propuesta separada que conserve ComboProducto y los nombres del v1 | Se creó una propuesta sin sustituir el v2 vigente ni modificar el código; solo marca tres cambios estructurales inevitables y limita el resto a atributos y métodos | `docs/diagrama_v2_propuesta_minima.png`, `docs/diagrama_v2_propuesta_minima.mmd`, `docs/reporte_propuesta_cambios_minimos.md` | Pendiente |
| 8 | 24/11/2026 | ChatGPT Codex | Adaptación integral del código | "listo, que sea el oficial, que sea el diagrama v2, y a partir de ahí que se haga el código" | Adaptar nombres, relaciones, validaciones y pruebas al modelo aprobado | Se implementó `ComboProducto`, se usaron `Local`, `ParaLlevar`, `Delivery`, `Efectivo`, `QR` y `Tarjeta`, se corrigieron validaciones críticas y se ampliaron las pruebas a doce casos | `modelo/`, `main.py`, `persistencia.py`, `pruebas.py` | Pendiente |
| 9 | 24/11/2026 | ChatGPT Codex | Ajuste final según fotografía | "usa ese modelo tal cual, no hagas mas nada, usalo para hacer el codigo" | Usar la fotografía final sin agregar clases ni relaciones | La fotografía reemplazó al v2 digital, se retiraron propuestas redundantes y la coordinación general pasó a funciones para no agregar una clase ausente del papel | `docs/diagrama_v2.png`, `restaurante.py`, documentación | Pendiente |

## Declaración

Declaro que este registro incluye los usos de IA realizados en el proyecto y que revisaré cada archivo hasta poder explicar y modificar el código sin ayuda.

Firma: ______________________________

