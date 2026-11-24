# Revisión del diagrama de clases v1

Esta revisión conserva el diagrama realizado en aula y sellado por el docente. La fotografía aprobada se guarda sin alteraciones en `docs/diagrama_v1.png`. Los ajustes se aplican únicamente en el diagrama v2 y deberán explicarse durante la defensa.

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
6. Las subclases deben utilizar nombres en PascalCase: `Local`, `ParaLlevar`, `Delivery`, `Efectivo`, `QR` y `Tarjeta`.
7. Todos los atributos y métodos deben incluir visibilidad, parámetros, tipos y retornos.
8. La versión final conserva solo las clases dibujadas en el papel; la coordinación general se resuelve fuera del modelo mediante funciones.
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
| Local | `Local` |
| Llevar | `ParaLlevar` |
| Delivery | `Delivery` |
| Pago | `MetodoPago` |
| Efectivo | `Efectivo` |
| Qr | `QR` |
| Tarjeta | `Tarjeta` |

## Variante confirmada

La variante asignada y confirmada es la A: descuento de combo del 10 %, Bs 2 por plato para llevar, envío gratuito desde Bs 150 únicamente en Cercado, pedido mínimo delivery de Bs 40 y chicharrón disponible solamente los domingos.
