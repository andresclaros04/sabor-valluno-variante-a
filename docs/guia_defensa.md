# Guía para la defensa individual

## Distribución de los 10 minutos

### Minutos 0 a 2 Diagrama v2

Explicar:

1. `Producto`, `Pedido` y `MetodoPago` son clases abstractas.
2. Cada jerarquía tiene tres subclases concretas.
3. `Combo` hereda de `Producto` y contiene dos o más objetos `Producto`.
4. `PedidoProducto` guarda un producto y su cantidad.
5. `restaurante.py` coordina productos, clientes y pedidos con funciones; no agrega una clase ausente del diagrama.
6. Los cambios respecto al v1 están en `cambios_v1_v2.md`.

### Minutos 2 a 5 Fragmento de código

Prepararse para explicar:

- Por qué se utiliza `ABC` y `@abstractmethod`.
- Cómo funciona un `@property` y su setter.
- Por qué `_items` y `_productos` no se entregan como listas modificables.
- Cómo `Combo.calcular_precio()` llama a `calcular_precio()` de cada producto.
- Cómo `ParaLlevar` cuenta platos dentro de combos sin preguntar su tipo.
- Cómo cada método de pago implementa `procesar_pago()`.

### Minutos 5 a 9 Cambio en vivo

#### Si el docente pide agregar Postre

1. Crear `Postre(Producto)`.
2. Agregar el atributo que indica si lleva crema.
3. Implementar `calcular_precio()` sumando Bs 3 cuando corresponda.
4. Implementar `esta_disponible()`.
5. Implementar `contar_platos()` devolviendo 0.
6. No modificar `Pedido`, `Combo` ni `ParaLlevar`.

El punto principal es demostrar que el polimorfismo permite añadir la clase sin cambiar los cálculos existentes.

#### Si el docente pide Tiquipaya

Agregar una entrada al diccionario `COSTOS_ENVIO` de `Delivery`:

```text
"tiquipaya": 18.0
```

No debería modificarse el resto del cálculo.

### Minuto 9 a 10 Traza

Caso de referencia de la variante A:

1. Silpancho: Bs 35.
2. Vaso de mocochinchi: Bs 6.
3. Subtotal del combo: `35 + 6 = 41`.
4. Descuento del 10 %: `41 × 0,10 = 4,10`.
5. Precio del combo: `41 - 4,10 = 36,90`.
6. Dos combos: `36,90 × 2 = 73,80`.
7. Envío a Quillacollo: Bs 15.
8. Total: `73,80 + 15 = 88,80`.

## Preguntas que debe poder responder

1. ¿Por qué `Combo` es un `Producto`?
2. ¿Por qué la cantidad está en `PedidoProducto` y no en `Producto`?
3. ¿Cómo se cuentan los envases de un plato dentro de un combo anidado?
4. ¿Por qué no se utiliza `isinstance()` para calcular precios o envases?
5. ¿Qué impide modificar la lista de productos desde fuera?
6. ¿Qué sucede al intentar cambiar directamente de `REGISTRADO` a `ENTREGADO`?
7. ¿Por qué delivery rechaza tarjeta?
8. ¿Dónde están las reglas específicas de la variante A?
9. ¿Cómo se evita que un combo se contenga a sí mismo?
10. ¿Por qué no se implementó el retraso de delivery? Respuesta: porque el docente decidió excluir esa regla y la decisión está registrada en el acta.

## Ensayo recomendado

Ejecutar `demo.py` para presentar el caso de referencia, ejecutar `pruebas.py`, elegir tres clases al azar y explicarlas línea por línea. Luego realizar una vez cada posible cambio en vivo y restaurar el archivo mediante Git.
