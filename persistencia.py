"""Guardado y carga opcional de los datos del sistema en JSON."""

from datetime import datetime
import json

from modelo.clientes import Cliente
from modelo.pagos import Efectivo, QR, Tarjeta
from modelo.pedidos import Delivery, Local, ParaLlevar, Pedido
from modelo.productos import Bebida, Combo, Plato
import restaurante as servicio


def _producto_a_diccionario(producto):
    if isinstance(producto, Plato):
        return {
            "clase": "Plato",
            "nombre": producto.nombre,
            "precio": producto.precio,
            "dias_disponibles": list(producto.dias_disponibles),
        }
    if isinstance(producto, Bebida):
        return {
            "clase": "Bebida",
            "nombre": producto.nombre,
            "precio": producto.precio,
            "tipo": producto.tipo,
            "presentacion": producto.presentacion,
        }
    if isinstance(producto, Combo):
        return {
            "clase": "Combo",
            "nombre": producto.nombre,
            "productos": [elemento.nombre for elemento in producto.productos],
        }
    raise TypeError("Hay un producto que no se puede guardar")


def _pago_a_diccionario(pago):
    if pago is None:
        return None
    if isinstance(pago, Efectivo):
        return {
            "clase": "Efectivo",
            "monto_recibido": pago.monto_recibido,
        }
    if isinstance(pago, QR):
        return {
            "clase": "QR",
            "codigo_transaccion": pago.codigo_transaccion,
        }
    if isinstance(pago, Tarjeta):
        return {"clase": "Tarjeta"}
    raise TypeError("Hay un método de pago que no se puede guardar")


def _pedido_a_diccionario(pedido):
    datos = {
        "numero": pedido.numero_pedido,
        "cliente_telefono": pedido.cliente.telefono,
        "fecha_registro": pedido.fecha_registro.isoformat(),
        "estado": pedido.estado,
        "items": [
            {
                "producto": item.producto.nombre,
                "cantidad": item.cantidad,
            }
            for item in pedido.items
        ],
        "pago": _pago_a_diccionario(pedido.pago),
    }
    if isinstance(pedido, Local):
        datos["clase"] = "Local"
        datos["mesa"] = pedido.mesa
    elif isinstance(pedido, ParaLlevar):
        datos["clase"] = "ParaLlevar"
    elif isinstance(pedido, Delivery):
        datos["clase"] = "Delivery"
        datos["zona"] = pedido.zona
    else:
        raise TypeError("Hay un pedido que no se puede guardar")
    return datos


def guardar_json(restaurante, ruta="datos.json"):
    datos = {
        "nombre": restaurante["nombre"],
        "variante": "A",
        "productos": [
            _producto_a_diccionario(producto)
            for producto in restaurante["productos"]
        ],
        "clientes": [
            {"nombre": cliente.nombre, "telefono": cliente.telefono}
            for cliente in restaurante["clientes"]
        ],
        "pedidos": [
            _pedido_a_diccionario(pedido) for pedido in restaurante["pedidos"]
        ],
    }
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def _cargar_productos(restaurante, productos_guardados):
    combos_pendientes = []
    for datos in productos_guardados:
        if datos["clase"] == "Plato":
            producto = Plato(
                datos["nombre"],
                datos["precio"],
                datos["dias_disponibles"],
            )
            servicio.registrar_producto(restaurante, producto)
        elif datos["clase"] == "Bebida":
            producto = Bebida(
                datos["nombre"],
                datos["precio"],
                datos["tipo"],
                datos["presentacion"],
            )
            servicio.registrar_producto(restaurante, producto)
        elif datos["clase"] == "Combo":
            combos_pendientes.append(datos)
        else:
            raise ValueError("El JSON contiene una clase de producto desconocida")

    while combos_pendientes:
        cantidad_anterior = len(combos_pendientes)
        for datos in list(combos_pendientes):
            try:
                productos = [
                    servicio.buscar_producto(restaurante, nombre)
                    for nombre in datos["productos"]
                ]
            except ValueError:
                continue
            servicio.registrar_producto(restaurante, Combo(datos["nombre"], productos))
            combos_pendientes.remove(datos)

        if len(combos_pendientes) == cantidad_anterior:
            raise ValueError("No se pueden resolver los productos de un combo")


def _crear_metodo_pago(datos):
    if datos is None:
        return None
    if datos["clase"] in {"Efectivo", "PagoEfectivo"}:
        return Efectivo(datos["monto_recibido"])
    if datos["clase"] in {"QR", "PagoQR"}:
        return QR(datos["codigo_transaccion"])
    if datos["clase"] in {"Tarjeta", "PagoTarjeta"}:
        return Tarjeta()
    raise ValueError("El JSON contiene un método de pago desconocido")


def _restaurar_estado(pedido, estado):
    if estado == Pedido.REGISTRADO:
        return
    if estado == Pedido.CANCELADO:
        pedido.cancelar()
        return

    pedido.cambiar_estado(Pedido.EN_PREPARACION)
    if estado == Pedido.EN_PREPARACION:
        return
    pedido.cambiar_estado(Pedido.LISTO)
    if estado == Pedido.LISTO:
        return

    pedido.cambiar_estado(Pedido.ENTREGADO)


def cargar_json(ruta="datos.json"):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if datos.get("variante") != "A":
        raise ValueError("El archivo no corresponde a la variante A")

    restaurante = servicio.crear_sistema(datos.get("nombre", "Sabor Valluno"))
    _cargar_productos(restaurante, datos.get("productos", []))

    for datos_cliente in datos.get("clientes", []):
        servicio.registrar_cliente(restaurante,
            Cliente(datos_cliente["nombre"], datos_cliente["telefono"])
        )

    for datos_pedido in datos.get("pedidos", []):
        cliente = servicio.buscar_cliente(restaurante, datos_pedido["cliente_telefono"])
        fecha = datetime.fromisoformat(datos_pedido["fecha_registro"])
        clase = datos_pedido["clase"]
        if clase in {"Local", "PedidoLocal"}:
            pedido = Local(
                datos_pedido["numero"], cliente, datos_pedido["mesa"], fecha
            )
        elif clase in {"ParaLlevar", "PedidoParaLlevar"}:
            pedido = ParaLlevar(datos_pedido["numero"], cliente, fecha)
        elif clase in {"Delivery", "PedidoDelivery"}:
            pedido = Delivery(
                datos_pedido["numero"], cliente, datos_pedido["zona"], fecha
            )
        else:
            raise ValueError("El JSON contiene un tipo de pedido desconocido")

        for datos_item in datos_pedido["items"]:
            producto = servicio.buscar_producto(restaurante, datos_item["producto"])
            pedido.agregar_producto(producto, datos_item["cantidad"])

        pago = _crear_metodo_pago(datos_pedido.get("pago"))
        if pago is not None:
            pedido.cobrar(pago)

        _restaurar_estado(pedido, datos_pedido["estado"])
        servicio.registrar_pedido(restaurante, pedido)

    return restaurante

