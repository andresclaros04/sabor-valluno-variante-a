"""Clase gestora del sistema de pedidos Sabor Valluno."""

from collections import Counter

from modelo.clientes import Cliente
from modelo.pedidos import Pedido
from modelo.productos import Producto


class Restaurante:
    def __init__(self, nombre="Sabor Valluno"):
        self._nombre = nombre
        self._productos = []
        self._clientes = []
        self._pedidos = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def productos(self):
        return tuple(self._productos)

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def pedidos(self):
        return tuple(self._pedidos)

    @property
    def siguiente_numero_pedido(self):
        if not self._pedidos:
            return 1
        return max(pedido.numero_pedido for pedido in self._pedidos) + 1

    def registrar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden registrar productos")
        if any(
            existente.nombre.lower() == producto.nombre.lower()
            for existente in self._productos
        ):
            raise ValueError("Ya existe un producto con ese nombre")
        self._productos.append(producto)

    def buscar_producto(self, nombre):
        for producto in self._productos:
            if producto.nombre.lower() == str(nombre).strip().lower():
                return producto
        raise ValueError("Producto no encontrado")

    def listar_menu_disponible(self, dia):
        return tuple(
            producto
            for producto in self._productos
            if producto.esta_disponible(dia)
        )

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise TypeError("Solo se pueden registrar clientes")
        if any(
            existente.telefono == cliente.telefono for existente in self._clientes
        ):
            raise ValueError("Ya existe un cliente con ese teléfono")
        self._clientes.append(cliente)

    def buscar_cliente(self, telefono):
        telefono = str(telefono).strip()
        for cliente in self._clientes:
            if cliente.telefono == telefono:
                return cliente
        raise ValueError("Cliente no encontrado")

    def mesa_disponible(self, mesa):
        return not any(
            pedido.numero_mesa == mesa and pedido.esta_abierto
            for pedido in self._pedidos
        )

    def registrar_pedido(self, pedido):
        if not isinstance(pedido, Pedido):
            raise TypeError("Solo se pueden registrar pedidos")
        if any(
            existente.numero_pedido == pedido.numero_pedido
            for existente in self._pedidos
        ):
            raise ValueError("El número de pedido ya existe")
        if pedido.numero_mesa is not None and not self.mesa_disponible(
            pedido.numero_mesa
        ):
            raise ValueError("La mesa ya tiene un pedido abierto")
        self._pedidos.append(pedido)

    def buscar_pedido(self, numero_pedido):
        for pedido in self._pedidos:
            if pedido.numero_pedido == numero_pedido:
                return pedido
        raise ValueError("Pedido no encontrado")

    def reporte_ventas(self, fecha):
        pedidos_pagados = [
            pedido
            for pedido in self._pedidos
            if pedido.metodo_pago is not None
            and pedido.fecha_registro.date() == fecha
        ]
        cantidades = Counter(pedido.tipo_pedido for pedido in pedidos_pagados)
        totales = Counter()
        for pedido in pedidos_pagados:
            totales[pedido.tipo_pedido] += pedido.calcular_total()

        return {
            "fecha": fecha.isoformat(),
            "cantidad_por_tipo": dict(cantidades),
            "total_por_tipo": {
                tipo: round(total, 2) for tipo, total in totales.items()
            },
            "total_general": round(
                sum(pedido.calcular_total() for pedido in pedidos_pagados), 2
            ),
            "productos_mas_vendidos": self.productos_mas_vendidos(
                pedidos_pagados, limite=3
            ),
        }

    def productos_mas_vendidos(self, pedidos=None, limite=3):
        pedidos = self._pedidos if pedidos is None else pedidos
        contador = Counter()
        for pedido in pedidos:
            if pedido.metodo_pago is None:
                continue
            for item in pedido.items:
                contador[item.producto.nombre] += item.cantidad
        return contador.most_common(limite)

