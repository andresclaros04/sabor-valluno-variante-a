# Guía de estudio paso a paso

## 1 Preparar VS Code

1. Abrir la carpeta `sabor_valluno`, no la carpeta general de tareas.
2. Comprobar que Python 3 esté seleccionado.
3. Abrir la terminal integrada.
4. Ejecutar `python pruebas.py` o `py pruebas.py`.
5. No continuar hasta obtener `Todas las pruebas superadas`.

## 2 Estudiar la jerarquía Producto

Archivo: `modelo/productos.py`.

### Producto

- Hereda de `ABC`.
- No se puede instanciar directamente.
- Encapsula `_nombre` y `_precio`.
- Los setters impiden nombres vacíos y precios no positivos.
- Declara los contratos `calcular_precio()`, `esta_disponible()` y `contar_platos()`.

Ejercicio: explicar por qué `Producto("Genérico", 10)` produce un error.

### Plato

- Hereda de `Producto` y llama `super().__init__()`.
- Conserva sus días disponibles.
- En la variante A, el chicharrón reemplaza cualquier lista recibida por domingo.
- Cuenta como un plato para los envases.

Ejercicio: crear un silpancho y comprobar su disponibilidad el lunes.

### Bebida

- El precio almacenado corresponde al vaso.
- La presentación solo puede ser vaso o jarra.
- La jarra multiplica el precio por tres.
- Una bebida cuenta como cero platos.

Ejercicio: cambiar la presentación de vaso a jarra y volver a calcular.

### Combo

- Hereda de `Producto`.
- Conserva una colección protegida de productos.
- La propiedad `productos` devuelve una tupla para impedir modificaciones externas.
- Calcula el precio llamando el mismo método de cada producto.
- Aplica el descuento de la variante A.
- Cuenta platos llamando `contar_platos()` de cada elemento.
- Detecta autorreferencias y ciclos mediante `contiene()`.

Ejercicio: seguir manualmente la ejecución de un combo que contiene otro combo.

## 3 Estudiar Cliente

Archivo: `modelo/clientes.py`.

- El nombre no puede estar vacío.
- El teléfono debe contener ocho dígitos.
- El primer dígito debe ser 6 o 7.

Ejercicio: probar teléfonos válidos e inválidos y anotar la excepción obtenida.

## 4 Estudiar PedidoProducto

Archivo: `modelo/pedidos.py`.

- Une un producto con una cantidad.
- La cantidad debe estar entre 1 y 20.
- Calcula el subtotal multiplicando precio por cantidad.
- Multiplica también el número de platos para calcular envases.

Esta clase explica por qué `cantidad` salió de `Producto` al pasar del diagrama v1 al v2.

## 5 Estudiar la jerarquía Pedido

### Pedido

- Es abstracta.
- Guarda cliente, fecha, estado, ítems, método de pago y comprobante.
- Solo permite agregar o quitar productos en `REGISTRADO`.
- Recorre polimórficamente sus ítems para obtener el subtotal.
- No permite transiciones de estado fuera del orden definido.
- No permite cobrar dos veces.

Ejercicio: intentar pasar directamente de `REGISTRADO` a `ENTREGADO`.

### PedidoLocal

- Guarda una mesa entre 1 y 15.
- No agrega cargos.
- `Restaurante` impide dos pedidos abiertos en la misma mesa.

### PedidoParaLlevar

- Cobra Bs 2 por cada plato.
- No pregunta si el producto es plato o combo.
- Llama `contar_platos()` y recibe la respuesta correspondiente.

Ejercicio: calcular los envases de dos combos que contienen un plato cada uno.

### PedidoDelivery

- Valida Cercado, Quillacollo, Sacaba y Vinto.
- Aplica pedido mínimo de Bs 40.
- Cercado tiene envío gratis desde Bs 150.
- Rechaza métodos de pago que no permitan delivery.
- No calcula retraso ni compensación porque el docente decidió excluir esa regla del proyecto; la decisión está registrada en el acta.

## 6 Estudiar los pagos

Archivo: `modelo/pagos.py`.

- `MetodoPago` declara el contrato `procesar_pago()`.
- `PagoEfectivo` comprueba el monto y calcula cambio.
- `PagoQR` exige diez dígitos.
- `PagoTarjeta` agrega 3 % y declara que no permite delivery.

Ejercicio: explicar cómo delivery rechaza tarjeta sin preguntar si el objeto es una tarjeta.

## 7 Estudiar Restaurante

Archivo: `restaurante.py`.

- Administra productos, clientes y pedidos.
- Controla nombres de producto y teléfonos duplicados.
- Comprueba la disponibilidad de mesas.
- Genera el reporte de ventas.
- Obtiene los tres productos más vendidos.

La clase gestora coordina objetos, pero no contiene los cálculos específicos de cada subclase.

## 8 Estudiar el menú

Archivo: `main.py`.

Recorrer cada opción en este orden:

1. Registrar dos productos.
2. Armar un combo.
3. Registrar un cliente.
4. Crear un pedido.
5. Agregar el combo.
6. Mostrar el detalle.
7. Cambiar el estado.
8. Cobrar.
9. Mostrar el reporte.
10. Guardar y cargar JSON.

## 9 Estudiar las pruebas

Archivo: `pruebas.py`.

No memorizar los resultados. Para cada `assert`, responder:

1. ¿Qué regla se está comprobando?
2. ¿Qué objeto se prepara?
3. ¿Qué método se ejecuta?
4. ¿Por qué ese resultado es correcto?
5. ¿Qué error detectaría si la prueba fallara?

## 10 Práctica diaria recomendada

1. Ejecutar las pruebas.
2. Explicar una clase sin leer comentarios.
3. Calcular un pedido a mano.
4. Cambiar temporalmente una regla.
5. Comprobar qué prueba falla.
6. Restaurar el cambio con Git.

No marcar “Sí” en el registro de IA hasta poder realizar estos pasos sin ayuda.

