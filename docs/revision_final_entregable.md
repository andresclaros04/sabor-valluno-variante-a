# Revisión final del entregable

Fecha de revisión: 23/11/2026

## Resultado general

El proyecto está técnicamente completo para solicitar revisión del docente. Compila, ejecuta las pruebas, reproduce el caso de referencia de la variante A y contiene los archivos mínimos indicados en la consigna. La publicación en GitHub se dejó intencionalmente para después del visto bueno.

## Evidencia revisada

| Criterio | Estado | Evidencia |
|---|---|---|
| Diagrama v1 | Cumple | `docs/diagrama_v1.png` conserva el modelado realizado en aula |
| Diagrama v2 | Cumple | `docs/diagrama_v2.png`, fotografía definitiva proporcionada por el estudiante |
| Cambios v1 a v2 | Cumple | `docs/cambios_v1_v2.md` |
| Encapsulación | Cumple | Atributos protegidos, propiedades y validaciones en `modelo/` |
| Herencia | Cumple | Tres jerarquías con nueve subclases concretas |
| Polimorfismo | Cumple | Precio, disponibilidad, platos, cargos y pagos se resuelven por métodos sobrescritos |
| Abstracción | Cumple | `Producto`, `Pedido` y `MetodoPago` utilizan `ABC` y `@abstractmethod` |
| Variante A | Cumple | 10 % de descuento, Bs 2 por plato, mínimo Bs 40, envío gratis en Cercado desde Bs 150 y chicharrón dominical |
| Regla de retraso | Cumple según decisión docente | El acta registra que no será evaluada y el código no la implementa |
| Menú de consola | Cumple | `main.py` contiene las funciones obligatorias |
| Reporte de ventas | Cumple | Ventas por tipo y tres productos más vendidos |
| Persistencia JSON | Cumple como opcional | `persistencia.py` y opciones 11 y 12 del menú |
| Pruebas | Cumple | 34 instrucciones `assert`; `pruebas.py` finaliza correctamente |
| Caso de referencia | Cumple | `demo.py` produce Bs 88,80 |
| Acta de consultas | Cumple | `docs/acta_consultas.md` no contiene respuestas pendientes |
| Documentación de IA | Requiere acción personal | Existen bitácora y registro, pero el estudiante debe completar su autoevaluación y firma |
| Historial Git | Cumple en cantidad | El repositorio local contiene 15 commits antes de esta revisión |
| GitHub | Pendiente intencionalmente | Se publicará después del visto bueno |

## Verificaciones ejecutadas

```text
python pruebas.py
Resultado: Todas las pruebas superadas
```

```text
python verificar_entrega.py
Resultado: archivos requeridos, pruebas funcionales y acta correctos
```

```text
python demo.py
Resultado: total de referencia Bs 88,80
```

El ZIP también se extrajo en una carpeta separada y las pruebas volvieron a pasar desde la copia extraída.

## Riesgos que no deben ocultarse

### Uso de IA durante una fase restringida

La consigna original indica que la semana 2 se realiza sin IA. La bitácora declara asistencia de IA para revisar y generar partes del proyecto. No se deben borrar ni modificar esos registros para aparentar otro proceso. Antes de entregar, el estudiante debe mostrar la bitácora al docente y solicitar su criterio.

### Distribución temporal de commits

El repositorio contiene suficientes commits en cantidad, pero varios fueron realizados durante una misma sesión de trabajo asistido. La consigna valora commits frecuentes y distribuidos. No se deben alterar fechas ni fabricar historial retroactivo. El estudiante debe continuar haciendo solamente commits reales de sus propias revisiones y ejercicios.

### Defensa individual

El mayor riesgo de calificación es no poder explicar o modificar el código. El estudiante debe completar `docs/guia_estudio_codigo.md` y `docs/guia_defensa.md`, ejecutar el proyecto personalmente y practicar los cambios `Postre` y `Tiquipaya` sin ayuda.

## Acciones obligatorias del estudiante

1. Ejecutar el proyecto en su propia instalación de VS Code.
2. Revisar línea por línea las clases seleccionadas para la defensa.
3. Completar “¿Lo explico sin ayuda?” con `Sí`, `Parcial` o `No` según corresponda.
4. Firmar `docs/registro_ia_claros.md`.
5. Consultar con el docente el uso de IA registrado durante la fase restringida.
6. Solicitar el visto bueno.
7. Publicar el repositorio públicamente solo después del visto bueno.
