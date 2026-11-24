"""Menú de consola del sistema Sabor Valluno."""

from datetime import date

from modelo.clientes import Cliente
from modelo.pagos import Efectivo, QR, Tarjeta
from modelo.pedidos import Delivery, Local, ParaLlevar, Pedido
from modelo.productos import Bebida, Combo, Plato
import restaurante as servicio
from persistencia import cargar_json, guardar_json


def leer_entero(mensaje):
    return int(input(mensaje).strip())


def leer_decimal(mensaje):
    return float(input(mensaje).strip().replace(",", "."))


def mostrar_productos(productos):
    if not productos:
        print("No hay productos registrados.")
        return
    for indice, producto in enumerate(productos, start=1):
        print(
            f"{indice}. {producto.nombre} - "
            f"Bs {producto.calcular_precio():.2f}"
        )


def mostrar_clientes(clientes):
    if not clientes:
        print("No hay clientes registrados.")
        return
    for indice, cliente in enumerate(clientes, start=1):
        print(f"{indice}. {cliente}")


def mostrar_pedidos(pedidos):
    if not pedidos:
        print("No hay pedidos registrados.")
        return
    for pedido in pedidos:
        print(
            f"Pedido {pedido.numero_pedido} | {pedido.tipo_pedido} | "
            f"{pedido.cliente.nombre} | {pedido.estado}"
        )


def seleccionar_producto(restaurante):
    mostrar_productos(restaurante["productos"])
    posicion = leer_entero("Número del producto: ") - 1
    if posicion < 0 or posicion >= len(restaurante["productos"]):
        raise ValueError("Selección de producto inválida")
    return restaurante["productos"][posicion]


def seleccionar_cliente(restaurante):
    mostrar_clientes(restaurante["clientes"])
    posicion = leer_entero("Número del cliente: ") - 1
    if posicion < 0 or posicion >= len(restaurante["clientes"]):
        raise ValueError("Selección de cliente inválida")
    return restaurante["clientes"][posicion]


def seleccionar_pedido(restaurante):
    mostrar_pedidos(restaurante["pedidos"])
    numero = leer_entero("Número del pedido: ")
    return servicio.buscar_pedido(restaurante, numero)


def registrar_producto(restaurante):
    print("\n1. Plato\n2. Bebida\n3. Combo")
    opcion = input("Tipo de producto: ").strip()
    nombre = input("Nombre: ").strip()

    if opcion == "1":
        precio = leer_decimal("Precio: Bs ")
        texto_dias = input(
            "Días disponibles separados por coma (vacío = todos): "
        ).strip()
        dias = None
        if texto_dias:
            dias = [dia.strip() for dia in texto_dias.split(",")]
        producto = Plato(nombre, precio, dias)
    elif opcion == "2":
        precio = leer_decimal("Precio por vaso: Bs ")
        tipo = input("Tipo de bebida: ").strip()
        presentacion = input("Presentación (vaso/jarra): ").strip()
        producto = Bebida(nombre, precio, tipo, presentacion)
    elif opcion == "3":
        mostrar_productos(restaurante["productos"])
        texto = input(
            "Números de al menos dos productos separados por coma: "
        ).strip()
        posiciones = [int(valor.strip()) - 1 for valor in texto.split(",")]
        productos = []
        for posicion in posiciones:
            if posicion < 0 or posicion >= len(restaurante["productos"]):
                raise ValueError("Uno de los productos seleccionados no existe")
            productos.append(restaurante["productos"][posicion])
        producto = Combo(nombre, productos)
    else:
        raise ValueError("Tipo de producto inválido")

    servicio.registrar_producto(restaurante, producto)
    print(f"Producto registrado: {producto.nombre}")


def listar_menu(restaurante):
    dia = input("Día de la semana: ").strip()
    disponibles = servicio.listar_menu_disponible(restaurante, dia)
    print(f"\nMenú disponible para {dia}:")
    mostrar_productos(disponibles)


def registrar_cliente(restaurante):
    nombre = input("Nombre del cliente: ").strip()
    telefono = input("Teléfono: ").strip()
    cliente = Cliente(nombre, telefono)
    servicio.registrar_cliente(restaurante, cliente)
    print(f"Cliente registrado: {cliente}")


def registrar_pedido(restaurante):
    cliente = seleccionar_cliente(restaurante)
    print("\n1. Local\n2. Para llevar\n3. Delivery")
    opcion = input("Tipo de pedido: ").strip()
    numero = servicio.siguiente_numero_pedido(restaurante)

    if opcion == "1":
        mesa = leer_entero("Mesa (1 a 15): ")
        if not servicio.mesa_disponible(restaurante, mesa):
            raise ValueError("La mesa ya tiene un pedido abierto")
        pedido = Local(numero, cliente, mesa)
    elif opcion == "2":
        pedido = ParaLlevar(numero, cliente)
    elif opcion == "3":
        zona = input("Zona (Cercado/Quillacollo/Sacaba/Vinto): ").strip()
        pedido = Delivery(numero, cliente, zona)
    else:
        raise ValueError("Tipo de pedido inválido")

    servicio.registrar_pedido(restaurante, pedido)
    print(f"Pedido {pedido.numero_pedido} registrado")


def agregar_producto_a_pedido(restaurante):
    pedido = seleccionar_pedido(restaurante)
    producto = seleccionar_producto(restaurante)
    cantidad = leer_entero("Cantidad (1 a 20): ")
    pedido.agregar_producto(producto, cantidad)
    print("Producto agregado al pedido")


def quitar_producto_de_pedido(restaurante):
    pedido = seleccionar_pedido(restaurante)
    if not pedido.items:
        raise ValueError("El pedido no tiene productos")
    for indice, item in enumerate(pedido.items, start=1):
        print(f"{indice}. {item.producto.nombre} x {item.cantidad}")
    posicion = leer_entero("Número del producto que desea quitar: ") - 1
    if posicion < 0 or posicion >= len(pedido.items):
        raise ValueError("Selección inválida")
    pedido.quitar_producto(pedido.items[posicion].producto)
    print("Producto retirado del pedido")


def mostrar_detalle(restaurante):
    pedido = seleccionar_pedido(restaurante)
    detalle = pedido.detalle()
    print(f"\nPedido {detalle['numero']} - {detalle['tipo']}")
    print(f"Cliente: {detalle['cliente']}")
    print(f"Estado: {detalle['estado']}")
    for item in detalle["items"]:
        print(
            f"- {item['producto']} x {item['cantidad']}: "
            f"Bs {item['subtotal']:.2f}"
        )
    print(f"Subtotal bruto: Bs {detalle['subtotal_bruto']:.2f}")
    print(f"Descuentos: Bs {detalle['descuentos']:.2f}")
    print(f"Subtotal con descuento: Bs {detalle['subtotal']:.2f}")
    print(f"Cargos: Bs {detalle['cargos']:.2f}")
    print(f"Total: Bs {detalle['total']:.2f}")


def cambiar_estado(restaurante):
    pedido = seleccionar_pedido(restaurante)
    print(
        "1. EN_PREPARACION\n"
        "2. LISTO\n"
        "3. ENTREGADO\n"
        "4. CANCELADO"
    )
    estados = {
        "1": Pedido.EN_PREPARACION,
        "2": Pedido.LISTO,
        "3": Pedido.ENTREGADO,
        "4": Pedido.CANCELADO,
    }
    opcion = input("Nuevo estado: ").strip()
    if opcion not in estados:
        raise ValueError("Opción de estado inválida")
    pedido.cambiar_estado(estados[opcion])
    print(f"Estado actualizado a {pedido.estado}")


def cobrar_pedido(restaurante):
    pedido = seleccionar_pedido(restaurante)
    print("\n1. Efectivo\n2. QR\n3. Tarjeta")
    opcion = input("Método de pago: ").strip()

    if opcion == "1":
        recibido = leer_decimal("Monto recibido: Bs ")
        metodo = Efectivo(recibido)
    elif opcion == "2":
        codigo = input("Código de transacción de 10 dígitos: ").strip()
        metodo = QR(codigo)
    elif opcion == "3":
        metodo = Tarjeta()
    else:
        raise ValueError("Método de pago inválido")

    comprobante = pedido.cobrar(metodo)
    print("\nComprobante")
    for clave, valor in comprobante.items():
        print(f"{clave}: {valor}")


def mostrar_reporte(restaurante):
    reporte = servicio.reporte_ventas(restaurante, date.today())
    print(f"\nReporte de ventas {reporte['fecha']}")
    print(f"Total general: Bs {reporte['total_general']:.2f}")
    for tipo, cantidad in reporte["cantidad_por_tipo"].items():
        total = reporte["total_por_tipo"][tipo]
        print(f"{tipo}: {cantidad} pedidos - Bs {total:.2f}")
    print("Tres productos más vendidos:")
    for nombre, cantidad in reporte["productos_mas_vendidos"]:
        print(f"- {nombre}: {cantidad}")


def guardar_datos(restaurante):
    ruta = input("Archivo JSON (vacío = datos.json): ").strip() or "datos.json"
    guardar_json(restaurante, ruta)
    print(f"Datos guardados en {ruta}")


def cargar_datos():
    ruta = input("Archivo JSON (vacío = datos.json): ").strip() or "datos.json"
    restaurante = cargar_json(ruta)
    print(f"Datos cargados desde {ruta}")
    return restaurante


def mostrar_menu_principal():
    print(
        "\n=== Sabor Valluno ===\n"
        "1. Registrar producto o combo\n"
        "2. Listar menú disponible\n"
        "3. Registrar cliente\n"
        "4. Registrar pedido\n"
        "5. Agregar producto a pedido\n"
        "6. Quitar producto de pedido\n"
        "7. Mostrar detalle de pedido\n"
        "8. Cambiar estado de pedido\n"
        "9. Cobrar pedido\n"
        "10. Mostrar reporte del día\n"
        "11. Guardar datos en JSON\n"
        "12. Cargar datos desde JSON\n"
        "0. Salir"
    )


def ejecutar():
    restaurante = servicio.crear_sistema()
    acciones = {
        "1": registrar_producto,
        "2": listar_menu,
        "3": registrar_cliente,
        "4": registrar_pedido,
        "5": agregar_producto_a_pedido,
        "6": quitar_producto_de_pedido,
        "7": mostrar_detalle,
        "8": cambiar_estado,
        "9": cobrar_pedido,
        "10": mostrar_reporte,
        "11": guardar_datos,
    }

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            print("Hasta luego")
            break
        if opcion == "12":
            try:
                restaurante = cargar_datos()
            except (ValueError, TypeError, OSError) as error:
                print(f"Error: {error}")
            continue
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción inválida")
            continue
        try:
            accion(restaurante)
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    ejecutar()

