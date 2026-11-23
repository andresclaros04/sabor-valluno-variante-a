# Cambios del diagrama v1 al v2

1. `Combo` pasa a heredar de `Producto`. Esto permite que un combo se use como cualquier otro producto y que pueda contener otros combos.
2. Se elimina `cantidad` de `Producto` y se coloca en `PedidoProducto`, porque la cantidad pertenece a una línea del pedido.
3. `ComboProductos` se reemplaza por la colección protegida `_productos` de `Combo` y por una composición `Combo 1` a `Producto 2..*`.
4. Se agregan a `Producto` los contratos abstractos `calcular_precio()`, `esta_disponible(dia)` y `contar_platos()`.
5. `Local`, `Llevar` y `Delivery` se renombran como `PedidoLocal`, `PedidoParaLlevar` y `PedidoDelivery`.
6. `Pedido` incorpora la colección de objetos `PedidoProducto`, la fecha de registro, el método de pago y las operaciones de subtotal, total y cobro.
7. `Pago` se renombra como `MetodoPago`; sus hijas se renombran `PagoEfectivo`, `PagoQR` y `PagoTarjeta`.
8. `MetodoPago` declara `procesar_pago()` y cada subclase implementa su comportamiento sin condicionales por tipo.
9. Se añade la clase gestora `Restaurante`, encargada de productos, clientes, pedidos, mesas y reportes.
10. Se agregan visibilidad, tipos, retornos y multiplicidades.
11. Se incorporan las reglas de la variante A: combo con 10 % de descuento, envase de Bs 2 por plato, pedido mínimo delivery de Bs 40, envío gratis en Cercado desde Bs 150 y chicharrón solo los domingos.
12. La regla de retraso y compensación queda pendiente de la respuesta registrada en el acta de consultas.

