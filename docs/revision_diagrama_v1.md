# Revisión del diagrama de clases v1

Esta revisión conserva el diagrama realizado en aula. Los ajustes se aplicarán en el diagrama v2 y deberán explicarse durante la defensa.

## Elementos presentes en el v1

- Clase abstracta `Producto`.
- Clases `Plato`, `Bebida` y `Combo`.
- Clase asociativa `ComboProductos`.
- Clase abstracta `Pedido`.
- Clases `Local`, `Llevar` y `Delivery`.
- Clase asociativa `PedidoProducto`.
- Clase `Cliente`.
- Clase abstracta `Pago`.
- Clases `Efectivo`, `Qr` y `Tarjeta`.
- Relaciones generales entre clientes, pedidos, productos y pagos.

## Correcciones que debe mostrar el v2

1. `Combo` debe heredar de `Producto`, porque un combo puede aparecer donde se espera cualquier producto y puede contener otros combos.
2. `Producto` no debe almacenar una cantidad del pedido. La cantidad corresponde a `PedidoProducto`.
3. `Producto` debe declarar los métodos abstractos `calcular_precio()`, `esta_disponible(dia)` y `contar_platos()`.
4. `Pedido` debe declarar `calcular_cargos()` como método abstracto.
5. `Pago` debe renombrarse a `MetodoPago` para coincidir con la consigna, y declarar `procesar_pago()` como método abstracto.
6. Las subclases deben utilizar nombres en PascalCase: `PedidoLocal`, `PedidoParaLlevar`, `PedidoDelivery`, `PagoEfectivo`, `PagoQR` y `PagoTarjeta`.
7. Todos los atributos y métodos deben incluir visibilidad, parámetros, tipos y retornos.
8. Debe añadirse la clase gestora `Restaurante` con relaciones y multiplicidades hacia productos, clientes y pedidos.
9. La composición de `Combo` con `Producto` debe indicar que contiene `2..*` productos.
10. `Pedido` debe componerse de `0..*` objetos `PedidoProducto`; cada `PedidoProducto` referencia exactamente un `Producto` y almacena su cantidad.
11. La relación `Cliente` a `Pedido` debe mostrar un cliente por pedido y cero o muchos pedidos por cliente.
12. El diagrama debe incluir al menos un atributo o método específico de la variante asignada.

## Correspondencia inicial para el código

| Elemento del v1 | Nombre previsto en el código |
|---|---|
| Producto | `Producto` |
| Plato | `Plato` |
| Bebida | `Bebida` |
| Combo | `Combo` |
| ComboProductos | Se representa mediante la colección protegida de productos de `Combo` |
| PedidoProducto | `PedidoProducto` |
| Pedido | `Pedido` |
| Local | `PedidoLocal` |
| Llevar | `PedidoParaLlevar` |
| Delivery | `PedidoDelivery` |
| Pago | `MetodoPago` |
| Efectivo | `PagoEfectivo` |
| Qr | `PagoQR` |
| Tarjeta | `PagoTarjeta` |

## Dato todavía necesario

La variante A, B, C, D, E o F debe confirmarse antes de implementar los cálculos. Este dato cambia el descuento del combo, los envases, el envío gratis, el pedido mínimo y una regla adicional.

