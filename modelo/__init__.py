"""Clases del modelo del sistema Sabor Valluno."""

from modelo.productos import Bebida, Combo, ComboProducto, Plato, Producto
from modelo.clientes import Cliente
from modelo.pagos import Efectivo, MetodoPago, QR, Tarjeta
from modelo.pedidos import (
    Pedido,
    Delivery,
    Local,
    ParaLlevar,
    PedidoProducto,
)

__all__ = [
    "Producto",
    "Plato",
    "Bebida",
    "Combo",
    "ComboProducto",
    "Cliente",
    "PedidoProducto",
    "Pedido",
    "Local",
    "ParaLlevar",
    "Delivery",
    "MetodoPago",
    "Efectivo",
    "QR",
    "Tarjeta",
]

