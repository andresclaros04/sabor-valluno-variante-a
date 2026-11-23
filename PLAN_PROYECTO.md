# Plan del proyecto Sabor Valluno

## Estado actual

- Semana 1: modelado en aula declarado como realizado por el estudiante.
- Diagrama v1: guardado en el formato requerido como `docs/diagrama_v1.png`; la fotografía JPG original también se conserva.
- Variante asignada: A.
- Regla de retraso y compensación: pendiente de respuesta del docente.
- Código: jerarquías principales, clase gestora, menú de consola y pruebas implementados.

## Semana 2 Productos y encapsulación

Entregable: jerarquía `Producto` con `Combo`, propiedades, validaciones y al menos cuatro commits.

1. Crear la clase abstracta `Producto`.
2. Implementar `Plato` y sus días de disponibilidad.
3. Implementar `Bebida` con vaso y jarra.
4. Implementar `Combo`, incluidos combos internos.
5. Encapsular atributos con propiedades y setters.
6. Validar nombre, precio, presentación, productos y autorreferencia del combo.
7. Aplicar exclusivamente la variante asignada.
8. Ejecutar pruebas manuales antes de cada commit.

Commits sugeridos:

1. `Crear clase abstracta Producto`
2. `Agregar Plato y Bebida con validaciones`
3. `Implementar Combo con productos anidados`
4. `Completar encapsulacion y reglas de variante`

## Semana 3 Pedidos polimorfismo y pagos

1. Implementar `Cliente` y validar el teléfono.
2. Crear la clase abstracta `Pedido`.
3. Implementar `PedidoLocal`, `PedidoParaLlevar` y `PedidoDelivery`.
4. Implementar estados y transiciones válidas.
5. Permitir modificar productos solamente en estado `REGISTRADO`.
6. Calcular subtotal, cargos y total sin condicionales por tipo de producto.
7. Crear la clase abstracta `MetodoPago`.
8. Implementar `PagoEfectivo`, `PagoQR` y `PagoTarjeta`.
9. Restringir tarjeta para pedidos delivery.
10. Aplicar la regla de retraso documentada por el docente.
11. Realizar al menos cuatro commits adicionales.

## Semana 4 Integración y defensa

1. Crear la clase gestora `Restaurante`.
2. Crear el menú de consola en `main.py`.
3. Registrar productos, combos, clientes y pedidos.
4. Mostrar detalle del pedido con subtotal, descuentos, cargos y total.
5. Cambiar estados y cobrar pedidos.
6. Mostrar comprobantes.
7. Generar reporte diario por tipo de pedido.
8. Mostrar los tres productos más vendidos.
9. Preparar ocho o más casos en `pruebas.py`.
10. Incluir el caso de referencia recalculado según la variante.
11. Probar un combo que contiene otro combo.
12. Preparar `docs/diagrama_v2.png` y explicar cambios respecto al v1.
13. Completar README, acta y bitácora.
14. Practicar la defensa y un cambio en vivo.

## Estructura final requerida

```text
sabor_valluno/
|-- modelo/
|   |-- __init__.py
|   |-- productos.py
|   |-- pedidos.py
|   |-- pagos.py
|   `-- clientes.py
|-- docs/
|   |-- diagrama_v1.png
|   |-- diagrama_v2.png
|   |-- bitacora_ia.md
|   |-- acta_consultas.md
|   `-- registro_ia_apellido.md
|-- restaurante.py
|-- main.py
|-- pruebas.py
`-- README.md
```

## Condiciones para iniciar el código

- Mantener todas las reglas alineadas con la variante A.
- Conservar el diagrama v1 original y trasladar las correcciones documentadas al v2.
- Confirmar con el docente si permite asistencia de IA durante la semana 2.
- Registrar la respuesta sobre retraso y compensación en el acta.

