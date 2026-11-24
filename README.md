# Sistema de Pedidos Sabor Valluno

Proyecto individual de Programación Orientada a Objetos desarrollado en Python con biblioteca estándar.

## Variante implementada

Variante A:

- Combo con 10 % de descuento.
- Envase de Bs 2 por cada plato para llevar, incluidos platos dentro de combos.
- Envío gratis desde Bs 150 solamente en Cercado.
- Pedido mínimo delivery de Bs 40.
- Chicharrón disponible solamente los domingos.

## Estructura

```text
sabor_valluno/
|-- modelo/
|   |-- __init__.py
|   |-- productos.py
|   |-- clientes.py
|   |-- pedidos.py
|   `-- pagos.py
|-- docs/
|   |-- diagrama_v1.png
|   |-- diagrama_v2.png
|   |-- cambios_v1_v2.md
|   |-- acta_consultas.md
|   |-- bitacora_ia.md
|   `-- registro_ia_claros.md
|-- restaurante.py
|-- persistencia.py
|-- main.py
|-- pruebas.py
`-- README.md
```

## Funcionalidades

- Registro de platos, bebidas y combos.
- Combos que pueden contener otros combos.
- Menú disponible por día.
- Registro y validación de clientes.
- Pedidos locales, para llevar y delivery.
- Modificación de productos solamente en estado `REGISTRADO`.
- Subtotal bruto, descuentos, subtotal descontado, cargos y total.
- Estados válidos y cancelación.
- Pagos en efectivo, QR y tarjeta.
- Restricción de tarjeta para delivery.
- Reporte diario por tipo de pedido.
- Tres productos más vendidos.
- Guardado y carga de productos, clientes, pedidos y pagos en JSON.
- Pruebas con `assert`.

## Pendientes inmediatos

1. Completar las respuestas del docente en `docs/acta_consultas.md`.
2. Revisar los ajustes propuestos en `docs/revision_diagrama_v1.md`.
3. Preparar el diagrama v2 final.
4. Conservar en el acta la decisión del docente de no evaluar retraso ni compensación.

## Ejecución

```text
python main.py
```

En Windows también puede ejecutarse con:

```text
py main.py
```

## Pruebas

```text
python pruebas.py
```

Resultado esperado:

```text
Todas las pruebas superadas
```

Antes de entregar también puede ejecutarse:

```text
python verificar_entrega.py
```

El verificador comprueba la estructura, ejecuta las pruebas y avisa si el acta conserva campos pendientes.

Para ensayar el caso de referencia sin introducir datos manualmente:

```text
python demo.py
```

Cuando el acta esté completa se puede crear el paquete final con:

```text
python crear_paquete_entrega.py
```

El script se negará a generar el ZIP si todavía encuentra campos marcados como `pendiente`.

## Diseño orientado a objetos

- Encapsulación mediante atributos protegidos, `@property` y setters.
- Herencia en las jerarquías `Producto`, `Pedido` y `MetodoPago`.
- Polimorfismo para precios, disponibilidad, conteo de platos, cargos y pagos.
- Abstracción mediante `ABC` y `@abstractmethod`.
- Composición de `Combo` con productos y de `Pedido` con `PedidoProducto`.
- Agregación de productos, clientes y pedidos en `Restaurante`.

## Decisión sobre retraso de delivery

El docente decidió no tomar en cuenta el tiempo de demora ni la compensación de delivery. La decisión está registrada en `docs/acta_consultas.md`, por lo que `PedidoDelivery` no contiene cálculos de penalización por tiempo.

El sistema utiliza únicamente la biblioteca estándar de Python durante su ejecución.

## Persistencia opcional

Las opciones 11 y 12 del menú guardan y cargan el estado en `datos.json`. El archivo conserva productos simples, combos anidados, clientes, pedidos, cantidades, estados y pagos.

