# Resultados de pruebas

Comando:

```text
python pruebas.py
```

Resultado verificado:

```text
Todas las pruebas superadas: 12 casos
```

## Casos cubiertos

1. Las tres clases madre (`Producto`, `Pedido` y `MetodoPago`) son abstractas.
2. Chicharrón solo está disponible el domingo y los precios son positivos.
3. La jarra cuesta tres veces el vaso.
4. `ComboProducto` relaciona realmente cada combo con sus productos.
5. Un combo anidado cuenta platos y envases de forma recursiva.
6. El caso de referencia de Quillacollo totaliza Bs 88,80.
7. Las cantidades y transiciones de estado inválidas se rechazan.
8. Delivery valida mínimo, zona, envío gratis y restricción de tarjeta.
9. Efectivo, QR y Tarjeta aplican sus reglas propias.
10. Una mesa no admite dos pedidos abiertos.
11. El reporte diario agrupa ventas y obtiene los tres más vendidos.
12. JSON conserva un pedido pagado que contiene un combo anidado.
