"""Casos de prueba del sistema Sabor Valluno.

Se ejecutan con: python pruebas.py
"""

from datetime import datetime

from modelo.clientes import Cliente
from modelo.pagos import PagoEfectivo, PagoQR, PagoTarjeta
from modelo.pedidos import (
    PedidoDelivery,
    PedidoLocal,
    PedidoParaLlevar,
)
from modelo.productos import Bebida, Combo, Plato, Producto
from restaurante import Restaurante


def verificar_excepcion(tipo_excepcion, funcion):
    try:
        funcion()
    except tipo_excepcion:
        return
    raise AssertionError(f"Se esperaba la excepción {tipo_excepcion.__name__}")


def probar_productos():
    verificar_excepcion(TypeError, lambda: Producto("Genérico", 10))
    verificar_excepcion(ValueError, lambda: Plato("Silpancho", 0))

    silpancho = Plato("Silpancho", 35)
    chicharron = Plato("Chicharrón", 45)
    mocochinchi = Bebida("Mocochinchi", 6, "refresco natural", "vaso")

    assert silpancho.esta_disponible("lunes")
    assert not chicharron.esta_disponible("sábado")
    assert chicharron.esta_disponible("domingo")
    assert silpancho.contar_platos() == 1

    assert mocochinchi.calcular_precio() == 6
    mocochinchi.presentacion = "jarra"
    assert mocochinchi.calcular_precio() == 18
    assert mocochinchi.contar_platos() == 0
    mocochinchi.presentacion = "vaso"

    combo = Combo("Combo valluno", [silpancho, mocochinchi])
    assert combo.calcular_precio() == 36.90
    assert combo.calcular_descuento() == 4.10
    assert combo.contar_platos() == 1

    combo_doble = Combo("Combo doble", [combo, silpancho])
    assert combo_doble.contar_platos() == 2
    assert combo_doble.esta_disponible("lunes")

    verificar_excepcion(ValueError, lambda: combo.agregar_producto(combo))


def crear_productos_referencia():
    silpancho = Plato("Silpancho", 35)
    mocochinchi = Bebida("Mocochinchi", 6, "refresco natural", "vaso")
    combo = Combo("Combo silpancho", [silpancho, mocochinchi])
    return silpancho, mocochinchi, combo


def probar_clientes_y_pedidos():
    verificar_excepcion(ValueError, lambda: Cliente("Ana", "51234567"))
    cliente = Cliente("Ana", "71234567")
    silpancho, _, combo = crear_productos_referencia()

    pedido_llevar = PedidoParaLlevar(
        1, cliente, datetime(2026, 11, 23, 12, 0)
    )
    pedido_llevar.agregar_producto(combo, 2)
    assert pedido_llevar.calcular_subtotal() == 73.80
    assert pedido_llevar.calcular_cargos() == 4.0
    assert pedido_llevar.calcular_total() == 77.80

    pedido_local = PedidoLocal(2, cliente, 5)
    pedido_local.agregar_producto(silpancho, 1)
    pedido_local.cambiar_estado(pedido_local.EN_PREPARACION)
    verificar_excepcion(
        ValueError, lambda: pedido_local.agregar_producto(silpancho, 1)
    )
    verificar_excepcion(
        ValueError, lambda: pedido_local.cambiar_estado(pedido_local.ENTREGADO)
    )


def probar_delivery_y_pagos():
    cliente = Cliente("Luis", "61234567")
    silpancho, _, combo = crear_productos_referencia()

    # Caso de referencia de la variante A.
    delivery = PedidoDelivery(
        3, cliente, "Quillacollo", datetime(2026, 11, 23, 12, 0)
    )
    delivery.agregar_producto(combo, 2)
    assert delivery.calcular_subtotal() == 73.80
    assert delivery.calcular_subtotal_bruto() == 82.00
    assert delivery.calcular_descuentos() == 8.20
    assert delivery.calcular_cargos() == 15.0
    assert delivery.calcular_total() == 88.80

    comprobante_qr = delivery.cobrar(PagoQR("1234567890"))
    assert comprobante_qr["total"] == 88.80
    verificar_excepcion(
        ValueError, lambda: delivery.cobrar(PagoTarjeta())
    )

    pedido_local = PedidoLocal(4, cliente, 3)
    pedido_local.agregar_producto(silpancho, 1)
    comprobante_efectivo = pedido_local.cobrar(PagoEfectivo(40))
    assert comprobante_efectivo["cambio"] == 5.0

    pedido_tarjeta = PedidoLocal(5, cliente, 4)
    pedido_tarjeta.agregar_producto(silpancho, 1)
    comprobante_tarjeta = pedido_tarjeta.cobrar(PagoTarjeta())
    assert comprobante_tarjeta["comision"] == 1.05
    assert comprobante_tarjeta["total"] == 36.05

    delivery_gratis = PedidoDelivery(6, cliente, "Cercado")
    delivery_gratis.agregar_producto(silpancho, 5)
    assert delivery_gratis.calcular_cargos() == 0.0

    delivery_pequeno = PedidoDelivery(7, cliente, "Cercado")
    delivery_pequeno.agregar_producto(silpancho, 1)
    verificar_excepcion(
        ValueError, lambda: delivery_pequeno.cobrar(PagoQR("0987654321"))
    )


def probar_restaurante():
    restaurante = Restaurante()
    cliente = Cliente("Rosa", "72345678")
    silpancho, mocochinchi, combo = crear_productos_referencia()

    restaurante.registrar_cliente(cliente)
    restaurante.registrar_producto(silpancho)
    restaurante.registrar_producto(mocochinchi)
    restaurante.registrar_producto(combo)

    pedido = PedidoLocal(1, cliente, 1)
    pedido.agregar_producto(combo, 2)
    pedido.cobrar(PagoEfectivo(100))
    restaurante.registrar_pedido(pedido)

    assert not restaurante.mesa_disponible(1)
    assert restaurante.productos_mas_vendidos() == [("Combo silpancho", 2)]
    reporte = restaurante.reporte_ventas(pedido.fecha_registro.date())
    assert reporte["cantidad_por_tipo"]["LOCAL"] == 1
    assert reporte["total_general"] == 73.80


if __name__ == "__main__":
    probar_productos()
    probar_clientes_y_pedidos()
    probar_delivery_y_pagos()
    probar_restaurante()
    print("Todas las pruebas superadas")
