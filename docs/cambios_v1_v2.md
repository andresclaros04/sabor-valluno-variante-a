# Reporte de cambios del diagrama v1 al v2

## Evidencia de partida

El diagrama v1 utilizado para esta comparación es la fotografía sellada por el docente y guardada como `docs/diagrama_v1.png`. El diagrama v2 conserva su organización visual:

- Productos en la zona superior.
- Pedido y sus tipos en la zona central.
- Método de pago y sus tipos en la zona inferior.
- Cliente a la izquierda.
- Clases hijas conectadas hacia su clase madre.
- Atributos y métodos separados dentro de cada caja.

El v1 no se corrige ni se reemplaza conceptualmente: se conserva como evidencia del modelado inicial. El v2 muestra su evolución para coincidir con la consigna y con el código.

## Cambios justificados

| N.º | En el diagrama v1 aprobado | En el diagrama v2 | Motivo del cambio | Correspondencia en el código |
|---:|---|---|---|---|
| 1 | `Combo` aparece como clase separada de `Producto`. | `Combo` hereda de `Producto`. | La consigna exige que un combo pueda contener productos, incluidos otros combos, y que calcule su precio polimórficamente. | `class Combo(Producto)` en `modelo/productos.py`. |
| 2 | `Producto` contiene `cantidad`. | La cantidad se mueve a `PedidoProducto`. | La cantidad depende de un pedido concreto; no es una característica permanente del producto. | `PedidoProducto._cantidad` en `modelo/pedidos.py`. |
| 3 | Existe la clase intermedia `ComboProducto`. | Se elimina esa clase y se dibuja la composición `Combo 1 ◆── 2..* Producto`. | El código conserva directamente una colección protegida de productos dentro de `Combo`. | `Combo._productos` en `modelo/productos.py`. |
| 4 | `Producto` no muestra un contrato completo. | Se agregan `calcular_precio()`, `esta_disponible(dia)` y `contar_platos()` como abstractos. | Las tres operaciones permiten calcular precios, disponibilidad y envases sin preguntar por el tipo concreto. | `Producto(ABC)` y `@abstractmethod` en `modelo/productos.py`. |
| 5 | Las hijas de Pedido se llaman `PLocal`, `PLlevar` y `PDelivery`. | Se llaman `PedidoLocal`, `PedidoParaLlevar` y `PedidoDelivery`. | Los nombres completos coinciden con la consigna y con las clases Python. | `modelo/pedidos.py`. |
| 6 | `PedidoProducto` contiene producto y pedido. | Contiene producto y cantidad; el pedido lo posee mediante composición. | Evita una referencia circular innecesaria y representa una línea del pedido. | `Pedido._items` y `PedidoProducto` en `modelo/pedidos.py`. |
| 7 | `Pedido` muestra número, estado y pago de forma general. | Agrega cliente, fecha, ítems, método de pago y operaciones de subtotal, descuentos, cargos, total, estados, cobro y detalle. | Son responsabilidades requeridas por el menú y las reglas funcionales. | Clase `Pedido` en `modelo/pedidos.py`. |
| 8 | `PLlevar` almacena número de envases. | `PedidoParaLlevar` almacena el costo por plato y calcula los envases recorriendo los productos. | Los envases dependen de los platos, incluso los contenidos dentro de combos. | `PedidoParaLlevar.calcular_cargos()`. |
| 9 | `PDelivery` muestra zona y cargo mínimo. | `PedidoDelivery` muestra zona, mínimo Bs 40, envío gratis desde Bs 150 en Cercado y sus operaciones. | Implementa los valores de la variante A. | Constantes y métodos de `PedidoDelivery`. |
| 10 | La clase madre se llama `Pago`; sus hijas son `PEfectivo`, `PQr` y `PTarjeta`. | Se usan `MetodoPago`, `PagoEfectivo`, `PagoQR` y `PagoTarjeta`. | Los nombres coinciden con la consigna y expresan claramente la jerarquía. | `modelo/pagos.py`. |
| 11 | `Pago` usa `validar_pago()`. | `MetodoPago` declara `procesar_pago(total)` como abstracto. | Cada forma de pago procesa el total y genera su propio comprobante mediante polimorfismo. | `MetodoPago.procesar_pago()` y sus sobrescrituras. |
| 12 | `Cliente` tiene nombre y teléfono sin tipos claros. | Se conservan ambos atributos con tipo `str` y visibilidad protegida. | El teléfono se valida con ocho dígitos y comienzo en 6 o 7. | `modelo/clientes.py`. |
| 13 | No existe una clase gestora. | Se agrega `Restaurante` y sus agregaciones con Producto, Cliente y Pedido. | La consigna exige una clase que gestione menú, clientes, pedidos, mesas y reportes. | `restaurante.py`. |
| 14 | Algunas relaciones usan `1` y `N` sin distinguir el tipo de relación. | Se emplean herencia, composición, agregación, asociación y multiplicidades `0..*`, `0..1` y `2..*`. | La rúbrica pide relaciones y multiplicidades completas. | Relaciones reales entre las colecciones y referencias del código. |
| 15 | No aparecen de forma completa las reglas de la variante. | Se señalan descuento 10 %, Bs 2 por plato, mínimo Bs 40, envío gratis desde Bs 150 en Cercado y disponibilidad dominical del chicharrón. | Son las reglas asignadas a la variante A. | `modelo/productos.py` y `modelo/pedidos.py`. |
| 16 | El v1 no define completamente la regla de retraso. | No se agregan retraso ni compensación. | El docente decidió que esos elementos no se tomarán en cuenta, decisión registrada en el acta. | `docs/acta_consultas.md`; no existe lógica de retraso en el código. |

## Elementos que se mantienen

- Las tres áreas principales: Producto, Pedido y Pago.
- `Plato`, `Bebida` y `Combo` como conceptos del menú.
- `Cliente` relacionado con pedidos.
- Los tres tipos de pedido.
- Las tres formas de pago.
- La lectura de herencia desde las clases hijas hacia la clase madre.
- La separación de cada caja en nombre, atributos y métodos.

## Criterio de correspondencia

El diagrama v2 representa las clases del dominio y su interfaz pública relevante. Los constructores, setters y métodos auxiliares protegidos utilizados internamente por Python no se repiten cuando no cambian la estructura del modelo. Las clases, nombres, atributos de negocio, métodos polimórficos y relaciones principales sí deben coincidir con el código.
