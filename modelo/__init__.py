"""Clases del modelo del sistema Sabor Valluno."""

from modelo.productos import Bebida, Combo, Plato, Producto
from modelo.clientes import Cliente
from modelo.pagos import MetodoPago, PagoEfectivo, PagoQR, PagoTarjeta
from modelo.pedidos import (
    Pedido,
    PedidoDelivery,
    PedidoLocal,
    PedidoParaLlevar,
    PedidoProducto,
)

__all__ = [
    "Producto",
    "Plato",
    "Bebida",
    "Combo",
    "Cliente",
    "PedidoProducto",
    "Pedido",
    "PedidoLocal",
    "PedidoParaLlevar",
    "PedidoDelivery",
    "MetodoPago",
    "PagoEfectivo",
    "PagoQR",
    "PagoTarjeta",
]

