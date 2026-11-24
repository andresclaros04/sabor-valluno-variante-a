"""Funciones de aplicación; no agrega clases al modelo UML aprobado."""

from collections import Counter

from modelo.clientes import Cliente
from modelo.pedidos import Pedido
from modelo.productos import Producto


def crear_sistema(nombre="Sabor Valluno"):
    return {"nombre": nombre, "productos": [], "clientes": [], "pedidos": []}


def siguiente_numero_pedido(sistema):
    if not sistema["pedidos"]:
        return 1
    return max(pedido.numero_pedido for pedido in sistema["pedidos"]) + 1


def registrar_producto(sistema, producto):
    if not isinstance(producto, Producto):
        raise TypeError("Solo se pueden registrar productos")
    if any(p.nombre.lower() == producto.nombre.lower() for p in sistema["productos"]):
        raise ValueError("Ya existe un producto con ese nombre")
    sistema["productos"].append(producto)


def buscar_producto(sistema, nombre):
    for producto in sistema["productos"]:
        if producto.nombre.lower() == str(nombre).strip().lower():
            return producto
    raise ValueError("Producto no encontrado")


def listar_menu_disponible(sistema, dia):
    return tuple(p for p in sistema["productos"] if p.esta_disponible(dia))


def registrar_cliente(sistema, cliente):
    if not isinstance(cliente, Cliente):
        raise TypeError("Solo se pueden registrar clientes")
    if any(c.telefono == cliente.telefono for c in sistema["clientes"]):
        raise ValueError("Ya existe un cliente con ese teléfono")
    sistema["clientes"].append(cliente)


def buscar_cliente(sistema, telefono):
    telefono = str(telefono).strip()
    for cliente in sistema["clientes"]:
        if cliente.telefono == telefono:
            return cliente
    raise ValueError("Cliente no encontrado")


def mesa_disponible(sistema, mesa):
    return not any(
        pedido.numero_mesa == mesa and pedido.esta_abierto
        for pedido in sistema["pedidos"]
    )


def registrar_pedido(sistema, pedido):
    if not isinstance(pedido, Pedido):
        raise TypeError("Solo se pueden registrar pedidos")
    if any(p.numero_pedido == pedido.numero_pedido for p in sistema["pedidos"]):
        raise ValueError("El número de pedido ya existe")
    if pedido.numero_mesa is not None and not mesa_disponible(sistema, pedido.numero_mesa):
        raise ValueError("La mesa ya tiene un pedido abierto")
    sistema["pedidos"].append(pedido)


def buscar_pedido(sistema, numero_pedido):
    for pedido in sistema["pedidos"]:
        if pedido.numero_pedido == numero_pedido:
            return pedido
    raise ValueError("Pedido no encontrado")


def productos_mas_vendidos(sistema, pedidos=None, limite=3):
    pedidos = sistema["pedidos"] if pedidos is None else pedidos
    contador = Counter()
    for pedido in pedidos:
        if pedido.pago is None:
            continue
        for item in pedido.items:
            contador[item.producto.nombre] += item.cantidad
    return contador.most_common(limite)


def reporte_ventas(sistema, fecha):
    pagados = [
        pedido for pedido in sistema["pedidos"]
        if pedido.pago is not None and pedido.fecha_registro.date() == fecha
    ]
    cantidades = Counter(pedido.tipo_pedido for pedido in pagados)
    totales = Counter()
    for pedido in pagados:
        totales[pedido.tipo_pedido] += pedido.calcular_total()
    return {
        "fecha": fecha.isoformat(),
        "cantidad_por_tipo": dict(cantidades),
        "total_por_tipo": {tipo: round(total, 2) for tipo, total in totales.items()},
        "total_general": round(sum(p.calcular_total() for p in pagados), 2),
        "productos_mas_vendidos": productos_mas_vendidos(sistema, pagados, 3),
    }
