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
|   |-- diagrama_v1.jpg
|   |-- diagrama_v2.png
|   |-- cambios_v1_v2.md
|   |-- acta_consultas.md
|   |-- bitacora_ia.md
|   `-- registro_ia_claros.md
|-- restaurante.py
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
- Pruebas con `assert`.

## Pendientes inmediatos

1. Completar las respuestas del docente en `docs/acta_consultas.md`.
2. Revisar los ajustes propuestos en `docs/revision_diagrama_v1.md`.
3. Preparar el diagrama v2 final.
4. Confirmar la regla de retraso y compensación antes de cerrar el proyecto.

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

## Diseño orientado a objetos

- Encapsulación mediante atributos protegidos, `@property` y setters.
- Herencia en las jerarquías `Producto`, `Pedido` y `MetodoPago`.
- Polimorfismo para precios, disponibilidad, conteo de platos, cargos y pagos.
- Abstracción mediante `ABC` y `@abstractmethod`.
- Composición de `Combo` con productos y de `Pedido` con `PedidoProducto`.
- Agregación de productos, clientes y pedidos en `Restaurante`.

## Regla pendiente de consulta

La cantidad de minutos que define un retraso y la compensación correspondiente deben completarse en `docs/acta_consultas.md`. El código no inventa esos valores y exige configurarlos antes de calcular una compensación.

El sistema utiliza únicamente la biblioteca estándar de Python durante su ejecución.

