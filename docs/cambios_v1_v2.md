# Reporte de cambios del diagrama v1 al v2

## Fuente oficial

El archivo `docs/diagrama_v2.png` es la fotografía definitiva proporcionada por el estudiante el 24/11/2026. No se redibujó ni se añadieron clases. El código se adaptó a ese modelo.

## Cambios estructurales conservados

1. `Combo` hereda de la clase abstracta `Producto`, igual que `Plato` y `Bebida`.
2. Se conserva `ComboProducto` como clase asociativa entre un combo y sus productos.
3. Se conserva `PedidoProducto` como relación entre un pedido, un producto y su cantidad.
4. `Pedido` mantiene las hijas `Local`, `ParaLlevar` y `Delivery`.
5. `MetodoPago` mantiene las hijas `Efectivo`, `QR` y `Tarjeta`.

## Cambios de atributos y métodos reflejados en el código

- `Combo` guarda descuento y productos; calcula precio, descuento y cantidad de platos.
- `Plato` guarda días disponibles.
- `Bebida` guarda tipo y presentación.
- `Pedido` agrega o quita productos, calcula subtotal, cargos y total, controla estados, cancela y cobra.
- `Local` valida mesa de 1 a 15.
- `ParaLlevar` cobra Bs 2 por cada plato, incluidos los contenidos en combos anidados.
- `Delivery` valida zona, pedido mínimo de Bs 40 y envío gratis en Cercado desde Bs 150.
- `Efectivo` calcula cambio; `QR` valida diez dígitos; `Tarjeta` calcula 3 % de comisión.

## Decisión para no contradecir el papel

No existe una clase adicional de gestión. El archivo `restaurante.py` contiene funciones de aplicación para registrar, buscar, controlar mesas y generar reportes. Estas funciones coordinan los objetos sin modificar el conjunto de clases del diagrama.

## Correcciones de consistencia y seguridad

- Se rechazan cantidades negativas incluso al acumular un producto existente.
- Un pedido vacío no puede pasar a preparación.
- Un delivery menor a Bs 40 no puede pasar a preparación ni cobrarse.
- Un pedido pagado no puede cancelarse ni cobrarse de nuevo.
- Se incluyen doce casos de prueba, el caso de Bs 88,80 y un combo anidado.
