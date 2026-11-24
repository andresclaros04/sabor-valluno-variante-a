"""Guardado y carga opcional de los datos del sistema en JSON."""

from datetime import datetime
import json

from modelo.clientes import Cliente
from modelo.pagos import PagoEfectivo, PagoQR, PagoTarjeta
from modelo.pedidos import Pedido, PedidoDelivery, PedidoLocal, PedidoParaLlevar
from modelo.productos import Bebida, Combo, Plato
from restaurante import Restaurante


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


def _pago_a_diccionario(metodo_pago):
    if metodo_pago is None:
        return None
    if isinstance(metodo_pago, PagoEfectivo):
        return {
            "clase": "PagoEfectivo",
            "monto_recibido": metodo_pago.monto_recibido,
        }
    if isinstance(metodo_pago, PagoQR):
        return {
            "clase": "PagoQR",
            "codigo_transaccion": metodo_pago.codigo_transaccion,
        }
    if isinstance(metodo_pago, PagoTarjeta):
        return {"clase": "PagoTarjeta"}
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
        "pago": _pago_a_diccionario(pedido.metodo_pago),
    }
    if isinstance(pedido, PedidoLocal):
        datos["clase"] = "PedidoLocal"
        datos["mesa"] = pedido.mesa
    elif isinstance(pedido, PedidoParaLlevar):
        datos["clase"] = "PedidoParaLlevar"
    elif isinstance(pedido, PedidoDelivery):
        datos["clase"] = "PedidoDelivery"
        datos["zona"] = pedido.zona
    else:
        raise TypeError("Hay un pedido que no se puede guardar")
    return datos


def guardar_json(restaurante, ruta="datos.json"):
    datos = {
        "nombre": restaurante.nombre,
        "variante": "A",
        "productos": [
            _producto_a_diccionario(producto)
            for producto in restaurante.productos
        ],
        "clientes": [
            {"nombre": cliente.nombre, "telefono": cliente.telefono}
            for cliente in restaurante.clientes
        ],
        "pedidos": [
            _pedido_a_diccionario(pedido) for pedido in restaurante.pedidos
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
            restaurante.registrar_producto(producto)
        elif datos["clase"] == "Bebida":
            producto = Bebida(
                datos["nombre"],
                datos["precio"],
                datos["tipo"],
                datos["presentacion"],
            )
            restaurante.registrar_producto(producto)
        elif datos["clase"] == "Combo":
            combos_pendientes.append(datos)
        else:
            raise ValueError("El JSON contiene una clase de producto desconocida")

    while combos_pendientes:
        cantidad_anterior = len(combos_pendientes)
        for datos in list(combos_pendientes):
            try:
                productos = [
                    restaurante.buscar_producto(nombre)
                    for nombre in datos["productos"]
                ]
            except ValueError:
                continue
            restaurante.registrar_producto(Combo(datos["nombre"], productos))
            combos_pendientes.remove(datos)

        if len(combos_pendientes) == cantidad_anterior:
            raise ValueError("No se pueden resolver los productos de un combo")


def _crear_metodo_pago(datos):
    if datos is None:
        return None
    if datos["clase"] == "PagoEfectivo":
        return PagoEfectivo(datos["monto_recibido"])
    if datos["clase"] == "PagoQR":
        return PagoQR(datos["codigo_transaccion"])
    if datos["clase"] == "PagoTarjeta":
        return PagoTarjeta()
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

    restaurante = Restaurante(datos.get("nombre", "Sabor Valluno"))
    _cargar_productos(restaurante, datos.get("productos", []))

    for datos_cliente in datos.get("clientes", []):
        restaurante.registrar_cliente(
            Cliente(datos_cliente["nombre"], datos_cliente["telefono"])
        )

    for datos_pedido in datos.get("pedidos", []):
        cliente = restaurante.buscar_cliente(datos_pedido["cliente_telefono"])
        fecha = datetime.fromisoformat(datos_pedido["fecha_registro"])
        clase = datos_pedido["clase"]
        if clase == "PedidoLocal":
            pedido = PedidoLocal(
                datos_pedido["numero"], cliente, datos_pedido["mesa"], fecha
            )
        elif clase == "PedidoParaLlevar":
            pedido = PedidoParaLlevar(datos_pedido["numero"], cliente, fecha)
        elif clase == "PedidoDelivery":
            pedido = PedidoDelivery(
                datos_pedido["numero"], cliente, datos_pedido["zona"], fecha
            )
        else:
            raise ValueError("El JSON contiene un tipo de pedido desconocido")

        for datos_item in datos_pedido["items"]:
            producto = restaurante.buscar_producto(datos_item["producto"])
            pedido.agregar_producto(producto, datos_item["cantidad"])

        metodo_pago = _crear_metodo_pago(datos_pedido.get("pago"))
        if metodo_pago is not None:
            pedido.cobrar(metodo_pago)

        _restaurar_estado(pedido, datos_pedido["estado"])
        restaurante.registrar_pedido(pedido)

    return restaurante

