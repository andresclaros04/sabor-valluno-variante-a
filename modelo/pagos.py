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
        self._monto_pagado = 0.0

    @property
    def monto_pagado(self):
        return self._monto_pagado

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


class PagoEfectivo(MetodoPago):
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
        self._monto_pagado = total
        return {
            "metodo": self.nombre,
            "total": total,
            "recibido": self.monto_recibido,
            "cambio": cambio,
        }


class PagoQR(MetodoPago):
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
        self._monto_pagado = total
        return {
            "metodo": self.nombre,
            "total": total,
            "codigo_transaccion": self.codigo_transaccion,
        }


class PagoTarjeta(MetodoPago):
    COMISION = 0.03

    def __init__(self):
        super().__init__()
        self._porcentaje_comision = self.COMISION

    @property
    def nombre(self):
        return "Tarjeta"

    @property
    def permite_delivery(self):
        return False

    @property
    def porcentaje_comision(self):
        return self._porcentaje_comision

    def calcular_comision(self, total):
        total = validar_total(total)
        return round(total * self.porcentaje_comision, 2)

    def procesar_pago(self, total):
        total = validar_total(total)
        comision = self.calcular_comision(total)
        total_con_comision = round(total + comision, 2)
        self._monto_pagado = total_con_comision
        return {
            "metodo": self.nombre,
            "subtotal_cobro": total,
            "comision": comision,
            "total": total_con_comision,
        }

