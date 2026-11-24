"""Jerarquía de pedidos y reglas de la variante A."""

from abc import ABC, abstractmethod
from datetime import datetime
import operator

DIAS_POR_INDICE = (
    "lunes",
    "martes",
    "miercoles",
    "jueves",
    "viernes",
    "sabado",
    "domingo",
)


def validar_producto(producto):
    """Valida el contrato de Producto sin preguntar por la subclase concreta."""
    try:
        producto.nombre
        producto.calcular_precio
        producto.esta_disponible
        producto.contar_platos
    except AttributeError as error:
        raise TypeError("El objeto no cumple el contrato de Producto") from error


class PedidoProducto:
    """Relaciona un producto con la cantidad solicitada."""

    def __init__(self, producto, cantidad):
        validar_producto(producto)
        self._producto = producto
        self.cantidad = cantidad

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if valor is True or valor is False:
            raise TypeError("La cantidad debe ser un número entero")
        try:
            valor = operator.index(valor)
        except TypeError as error:
            raise TypeError("La cantidad debe ser un número entero") from error
        if not 1 <= valor <= 20:
            raise ValueError("La cantidad debe estar entre 1 y 20")
        self._cantidad = valor

    def calcular_subtotal(self):
        return round(self.producto.calcular_precio() * self.cantidad, 2)

    def _calcular_descuento(self):
        return round(self.producto._calcular_descuento() * self.cantidad, 2)

    def contar_platos(self):
        return self.producto.contar_platos() * self.cantidad


class Pedido(ABC):
    REGISTRADO = "REGISTRADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

    TRANSICIONES = {
        REGISTRADO: {EN_PREPARACION, CANCELADO},
        EN_PREPARACION: {LISTO},
        LISTO: {ENTREGADO},
        ENTREGADO: set(),
        CANCELADO: set(),
    }

    def __init__(self, numero_pedido, cliente, fecha_registro=None):
        if numero_pedido is True or numero_pedido is False:
            raise TypeError("El número de pedido debe ser entero")
        try:
            numero_pedido = operator.index(numero_pedido)
        except TypeError as error:
            raise TypeError("El número de pedido debe ser entero") from error
        if numero_pedido <= 0:
            raise ValueError("El número de pedido debe ser positivo")
        try:
            cliente.nombre
            cliente.telefono
        except AttributeError as error:
            raise TypeError("El pedido requiere un cliente válido") from error

        self._numero_pedido = numero_pedido
        self._cliente = cliente
        self._fecha_registro = fecha_registro or datetime.now()
        self._estado = self.REGISTRADO
        self._items = []
        self._pago = None
        self._comprobante = None

    @property
    def numero_pedido(self):
        return self._numero_pedido

    @property
    def cliente(self):
        return self._cliente

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @property
    def dia(self):
        return DIAS_POR_INDICE[self.fecha_registro.weekday()]

    @property
    def estado(self):
        return self._estado

    @property
    def items(self):
        return tuple(self._items)

    @property
    def pago(self):
        return self._pago

    @property
    def comprobante(self):
        return self._comprobante

    @property
    def esta_abierto(self):
        return self.estado not in {self.ENTREGADO, self.CANCELADO}

    @property
    def numero_mesa(self):
        return None

    @property
    @abstractmethod
    def tipo_pedido(self):
        """Nombre utilizado en reportes."""

    def _validar_modificable(self):
        if self.estado != self.REGISTRADO:
            raise ValueError("Solo se modifica un pedido en estado REGISTRADO")

    def agregar_producto(self, producto, cantidad=1):
        self._validar_modificable()
        validar_producto(producto)
        # Valida la cantidad incluso cuando el producto ya estaba agregado.
        cantidad_validada = PedidoProducto(producto, cantidad).cantidad
        if not producto.esta_disponible(self.dia):
            raise ValueError(f"{producto.nombre} no está disponible el {self.dia}")

        for item in self._items:
            if item.producto is producto:
                item.cantidad = item.cantidad + cantidad_validada
                return
        self._items.append(PedidoProducto(producto, cantidad_validada))

    def quitar_producto(self, producto):
        self._validar_modificable()
        for item in self._items:
            if item.producto is producto:
                self._items.remove(item)
                return
        raise ValueError("El producto no pertenece al pedido")

    def calcular_subtotal(self):
        return round(sum(item.calcular_subtotal() for item in self._items), 2)

    def _calcular_descuentos(self):
        return round(sum(item._calcular_descuento() for item in self._items), 2)

    def _calcular_subtotal_bruto(self):
        return round(self.calcular_subtotal() + self._calcular_descuentos(), 2)

    @abstractmethod
    def calcular_cargos(self):
        """Calcula cargos específicos del tipo de pedido."""

    def calcular_total(self):
        return round(self.calcular_subtotal() + self.calcular_cargos(), 2)

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado not in self.TRANSICIONES:
            raise ValueError("El estado solicitado no existe")
        if nuevo_estado not in self.TRANSICIONES[self.estado]:
            raise ValueError(
                f"No se puede cambiar de {self.estado} a {nuevo_estado}"
            )
        if nuevo_estado == self.EN_PREPARACION:
            if not self._items:
                raise ValueError("Un pedido sin productos no puede prepararse")
            self.validar_inicio_preparacion()
        self._estado = nuevo_estado

    def validar_inicio_preparacion(self):
        """Punto polimórfico para reglas previas a la preparación."""
        return True

    def cancelar(self):
        if self.pago is not None:
            raise ValueError("No se puede cancelar un pedido ya pagado")
        self.cambiar_estado(self.CANCELADO)

    def cobrar(self, pago):
        if not self._items:
            raise ValueError("No se puede cobrar un pedido sin productos")
        if self.estado == self.CANCELADO:
            raise ValueError("No se puede cobrar un pedido cancelado")
        if self.pago is not None:
            raise ValueError("El pedido ya fue pagado")
        try:
            comprobante = pago.procesar_pago(self.calcular_total())
        except AttributeError as error:
            raise TypeError("El objeto no cumple el contrato de MetodoPago") from error
        self._comprobante = comprobante
        self._pago = pago
        return dict(self._comprobante)

    def detalle(self):
        return {
            "numero": self.numero_pedido,
            "cliente": self.cliente.nombre,
            "tipo": self.tipo_pedido,
            "estado": self.estado,
            "items": [
                {
                    "producto": item.producto.nombre,
                    "cantidad": item.cantidad,
                    "subtotal": item.calcular_subtotal(),
                }
                for item in self._items
            ],
            "subtotal_bruto": self._calcular_subtotal_bruto(),
            "descuentos": self._calcular_descuentos(),
            "subtotal": self.calcular_subtotal(),
            "cargos": self.calcular_cargos(),
            "total": self.calcular_total(),
        }


class Local(Pedido):
    def __init__(self, numero_pedido, cliente, mesa, fecha_registro=None):
        super().__init__(numero_pedido, cliente, fecha_registro)
        self.mesa = mesa

    @property
    def tipo_pedido(self):
        return "LOCAL"

    @property
    def mesa(self):
        return self._mesa

    @mesa.setter
    def mesa(self, valor):
        if valor is True or valor is False:
            raise TypeError("La mesa debe ser un número entero")
        try:
            valor = operator.index(valor)
        except TypeError as error:
            raise TypeError("La mesa debe ser un número entero") from error
        if not 1 <= valor <= 15:
            raise ValueError("La mesa debe estar entre 1 y 15")
        self._mesa = valor

    @property
    def numero_mesa(self):
        return self.mesa

    def calcular_cargos(self):
        return 0.0


class ParaLlevar(Pedido):
    COSTO_ENVASE_POR_PLATO = 2.0

    def __init__(self, numero_pedido, cliente, fecha_registro=None):
        super().__init__(numero_pedido, cliente, fecha_registro)
        self._costo_envase_por_plato = self.COSTO_ENVASE_POR_PLATO

    @property
    def costo_envase_por_plato(self):
        return self._costo_envase_por_plato

    @property
    def tipo_pedido(self):
        return "PARA_LLEVAR"

    def calcular_cargos(self):
        cantidad_platos = sum(item.contar_platos() for item in self._items)
        return round(cantidad_platos * self.costo_envase_por_plato, 2)


class Delivery(Pedido):
    COSTOS_ENVIO = {
        "cercado": 8.0,
        "quillacollo": 15.0,
        "sacaba": 15.0,
        "vinto": 20.0,
    }
    PEDIDO_MINIMO = 40.0
    ENVIO_GRATIS_CERCADO_DESDE = 150.0

    def __init__(self, numero_pedido, cliente, zona, fecha_registro=None):
        super().__init__(numero_pedido, cliente, fecha_registro)
        self._pedido_minimo = self.PEDIDO_MINIMO
        self._envio_gratis_desde = self.ENVIO_GRATIS_CERCADO_DESDE
        self.zona = zona

    @property
    def tipo_pedido(self):
        return "DELIVERY"

    @property
    def zona(self):
        return self._zona

    @zona.setter
    def zona(self, valor):
        zona = str(valor).strip().lower()
        if zona not in self.COSTOS_ENVIO:
            raise ValueError("La zona de delivery no está registrada")
        self._zona = zona

    @property
    def pedido_minimo(self):
        return self._pedido_minimo

    @property
    def envio_gratis_desde(self):
        return self._envio_gratis_desde

    def calcular_cargos(self):
        if (
            self.zona == "cercado"
            and self.calcular_subtotal() >= self.envio_gratis_desde
        ):
            return 0.0
        return self.COSTOS_ENVIO[self.zona]

    def validar_pedido_minimo(self):
        if self.calcular_subtotal() < self.pedido_minimo:
            raise ValueError(
                f"El pedido mínimo para delivery es Bs {self.pedido_minimo:.2f}"
            )
        return True

    def validar_inicio_preparacion(self):
        return self.validar_pedido_minimo()

    def cobrar(self, pago):
        self.validar_pedido_minimo()
        if not pago.permite_delivery:
            raise ValueError("Delivery solo acepta efectivo o QR")
        return super().cobrar(pago)


