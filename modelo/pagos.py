"""Jerarquía de métodos de pago del restaurante."""

from abc import ABC, abstractmethod


def validar_total(total):
    if isinstance(total, bool) or not isinstance(total, (int, float)):
        raise TypeError("El total debe ser numérico")
    if total <= 0:
        raise ValueError("El total debe ser mayor que cero")
    return round(float(total), 2)


class MetodoPago(ABC):
    def __init__(self):
        self._monto = 0.0

    @property
    def monto(self):
        return self._monto

    @property
    @abstractmethod
    def nombre(self):
        """Nombre mostrado en el comprobante."""

    @property
    def permite_delivery(self):
        return True

    @abstractmethod
    def procesar_pago(self, total):
        """Procesa el pago y devuelve los datos del comprobante."""


class Efectivo(MetodoPago):
    def __init__(self, monto_recibido):
        super().__init__()
        if isinstance(monto_recibido, bool) or not isinstance(
            monto_recibido, (int, float)
        ):
            raise TypeError("El monto recibido debe ser numérico")
        if monto_recibido <= 0:
            raise ValueError("El monto recibido debe ser mayor que cero")
        self._monto_recibido = round(float(monto_recibido), 2)

    @property
    def nombre(self):
        return "Efectivo"

    @property
    def monto_recibido(self):
        return self._monto_recibido

    def calcular_cambio(self, total):
        total = validar_total(total)
        if self.monto_recibido < total:
            raise ValueError("El monto recibido no cubre el total")
        return round(self.monto_recibido - total, 2)

    def procesar_pago(self, total):
        total = validar_total(total)
        cambio = self.calcular_cambio(total)
        self._monto = total
        return {
            "metodo": self.nombre,
            "total": total,
            "recibido": self.monto_recibido,
            "cambio": cambio,
        }


class QR(MetodoPago):
    def __init__(self, codigo_transaccion):
        super().__init__()
        codigo = str(codigo_transaccion).strip()
        if len(codigo) != 10 or not codigo.isdigit():
            raise ValueError("El código QR debe tener exactamente 10 dígitos")
        self._codigo_transaccion = codigo

    @property
    def nombre(self):
        return "QR"

    @property
    def codigo_transaccion(self):
        return self._codigo_transaccion

    def procesar_pago(self, total):
        total = validar_total(total)
        self._monto = total
        return {
            "metodo": self.nombre,
            "total": total,
            "codigo_transaccion": self.codigo_transaccion,
        }


class Tarjeta(MetodoPago):
    COMISION = 0.03

    def __init__(self):
        super().__init__()
        self._comision = self.COMISION

    @property
    def nombre(self):
        return "Tarjeta"

    @property
    def permite_delivery(self):
        return False

    @property
    def comision(self):
        return self._comision

    def calcular_comision(self, total):
        total = validar_total(total)
        return round(total * self.comision, 2)

    def procesar_pago(self, total):
        total = validar_total(total)
        comision = self.calcular_comision(total)
        total_con_comision = round(total + comision, 2)
        self._monto = total_con_comision
        return {
            "metodo": self.nombre,
            "subtotal_cobro": total,
            "comision": comision,
            "total": total_con_comision,
        }

