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
|   |-- diagrama_v1.png
|   |-- diagrama_v2.png
|   |-- cambios_v1_v2.md
|   |-- acta_consultas.md
|   |-- bitacora_ia.md
|   `-- registro_ia_claros.md
|-- restaurante.py
|-- persistencia.py
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
- Guardado y carga de productos, clientes, pedidos y pagos en JSON.
- Pruebas con `assert`.

## Estado del entregable

El código, las pruebas, el acta, los diagramas y la documentación técnica están completos. Antes de solicitar el visto bueno, el estudiante debe:

1. Ejecutar personalmente `main.py`, `demo.py`, `pruebas.py` y `verificar_entrega.py` en VS Code.
2. Completar honestamente la columna “¿Lo explico sin ayuda?” del registro de IA.
3. Firmar el registro personal de IA.
4. Practicar la defensa y los cambios en vivo.
5. Consultar con el docente el uso de IA realizado durante una fase inicialmente indicada como “sin IA”.
6. Publicar en GitHub solamente después de recibir el visto bueno.

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
Todas las pruebas superadas: 12 casos
```

Antes de entregar también puede ejecutarse:

```text
python verificar_entrega.py
```

El verificador comprueba la estructura, ejecuta las pruebas y confirma que el acta no conserve campos pendientes.

Para ensayar el caso de referencia sin introducir datos manualmente:

```text
python demo.py
```

Para volver a crear el paquete final se utiliza:

```text
python crear_paquete_entrega.py
```

El script se negará a generar el ZIP si el acta vuelve a contener campos marcados como `pendiente`.

## Diseño orientado a objetos

- Encapsulación mediante atributos protegidos, `@property` y setters.
- Herencia en las jerarquías `Producto`, `Pedido` y `MetodoPago`.
- Polimorfismo para precios, disponibilidad, conteo de platos, cargos y pagos.
- Abstracción mediante `ABC` y `@abstractmethod`.
- Composición de `Combo` con productos y de `Pedido` con `PedidoProducto`.
- Coordinación de productos, clientes y pedidos mediante funciones de aplicación, sin agregar clases al diagrama.

## Decisión sobre retraso de delivery

El docente decidió no tomar en cuenta el tiempo de demora ni la compensación de delivery. La decisión está registrada en `docs/acta_consultas.md`, por lo que `Delivery` no contiene cálculos de penalización por tiempo.

El sistema utiliza únicamente la biblioteca estándar de Python durante su ejecución.

## Persistencia opcional

Las opciones 11 y 12 del menú guardan y cargan el estado en `datos.json`. El archivo conserva productos simples, combos anidados, clientes, pedidos, cantidades, estados y pagos.
