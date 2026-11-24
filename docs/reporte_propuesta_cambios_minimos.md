# Propuesta de cambios mínimos al diagrama aprobado

## Criterio

Esta propuesta no reemplaza todavía el diagrama v2 definitivo. Conserva la distribución, las clases y las relaciones principales del diagrama v1 sellado. Los cambios se limitan primero a atributos y métodos. Solo se proponen tres cambios estructurales porque la consigna los exige expresamente.

## Cambios estructurales inevitables

| Cambio | Por qué no puede resolverse solo con atributos o métodos |
|---|---|
| Agregar herencia de `Combo` hacia `Producto` | La consigna define la jerarquía Producto–Plato–Bebida–Combo y exige que un combo pueda contener otro combo mediante polimorfismo. |
| Renombrar `Pago` como `MetodoPago` | La consigna nombra así la clase abstracta y exige que los identificadores coincidan entre diagrama y código. La caja permanece en el mismo lugar. |
| Agregar `Restaurante` | La consigna exige una clase gestora con relaciones y multiplicidades hacia productos, clientes y pedidos. |

## Clases que se conservan

- `ComboProducto` se mantiene como en el v1. Representa la relación entre un combo y cada producto contenido.
- `PedidoProducto` se mantiene como clase de relación entre pedido y producto.
- `Cliente`, `Producto`, `Plato`, `Bebida`, `Pedido`, `Local`, `ParaLlevar`, `Delivery`, `Efectivo`, `QR` y `Tarjeta` mantienen su concepto y posición.

## Cambios limitados a atributos

1. En `Producto`, se elimina `cantidad` porque pertenece a una línea del pedido.
2. En `PedidoProducto`, el atributo `pedido` se reemplaza por `cantidad: int`; la relación con Pedido queda expresada por composición.
3. En `Combo`, se agrega `descuento = 0.10` y una colección de `ComboProducto`.
4. En `ParaLlevar`, se usa `costo_envase = 2` en lugar de almacenar un número fijo de envases.
5. En `Delivery`, se agregan zona, pedido mínimo 40 y envío gratis desde 150.
6. En `Tarjeta`, se fija la comisión en 0.03.
7. En `Cliente`, se conservan nombre y teléfono.

## Cambios limitados a métodos

1. `Producto` declara `calcular_precio()`, `esta_disponible(dia)` y `contar_platos()`.
2. `Combo`, `Plato` y `Bebida` sobrescriben esos tres métodos.
3. `Pedido` agrega las operaciones necesarias para añadir y quitar productos, calcular subtotales, cargos y total, cambiar estado, cancelar y cobrar.
4. `Local`, `ParaLlevar` y `Delivery` sobrescriben `calcular_cargos()`.
5. `MetodoPago` declara `procesar_pago()`; Efectivo, QR y Tarjeta lo sobrescriben.
6. `Restaurante` registra productos, clientes y pedidos y genera el reporte.

## Consecuencia para el código

El código todavía no debe modificarse hasta que esta propuesta sea aprobada. Después de la aprobación:

- Se conservará o implementará `ComboProducto`.
- Las subclases de Pedido se llamarán `Local`, `ParaLlevar` y `Delivery`.
- Las subclases de MetodoPago se llamarán `Efectivo`, `QR` y `Tarjeta`.
- El resto de la lógica se adaptará a estos nombres y relaciones.

Esto evita rehacer el modelado aprobado para obligarlo a coincidir con un código existente. El código será el que se adapte al diagrama.
