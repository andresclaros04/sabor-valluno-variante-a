"""Jerarquía de productos del restaurante Sabor Valluno."""

from abc import ABC, abstractmethod
import unicodedata


DIAS_VALIDOS = {
    "lunes",
    "martes",
    "miercoles",
    "jueves",
    "viernes",
    "sabado",
    "domingo",
}


def normalizar_texto(texto):
    """Devuelve texto en minúsculas y sin tildes para comparar valores."""
    texto_normalizado = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(
        caracter
        for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )


class Producto(ABC):
    """Contrato común para platos, bebidas y combos."""

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("El precio debe ser un número")
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        self._precio = round(float(valor), 2)

    @abstractmethod
    def calcular_precio(self):
        """Devuelve el precio actual del producto."""

    @abstractmethod
    def esta_disponible(self, dia):
        """Indica si el producto puede venderse en el día recibido."""

    @abstractmethod
    def contar_platos(self):
        """Devuelve cuántos platos contiene el producto."""

    def contiene(self, producto_buscado):
        """Permite detectar ciclos sin preguntar por el tipo concreto."""
        return self is producto_buscado

    def calcular_descuento(self):
        """Los productos simples no aplican descuento."""
        return 0.0


class Plato(Producto):
    """Producto que cuenta como plato y puede limitarse a ciertos días."""

    def __init__(self, nombre, precio, dias_disponibles=None):
        super().__init__(nombre, precio)

        # Regla adicional de la variante A.
        if normalizar_texto(nombre) == "chicharron":
            dias_disponibles = {"domingo"}

        if dias_disponibles is None:
            dias_disponibles = DIAS_VALIDOS
        self.dias_disponibles = dias_disponibles

    @property
    def dias_disponibles(self):
        return tuple(sorted(self._dias_disponibles))

    @dias_disponibles.setter
    def dias_disponibles(self, valores):
        dias = {normalizar_texto(dia) for dia in valores}
        if not dias:
            raise ValueError("Un plato debe tener al menos un día disponible")
        if not dias.issubset(DIAS_VALIDOS):
            raise ValueError("La lista contiene un día no válido")
        self._dias_disponibles = dias

    def calcular_precio(self):
        return self.precio

    def esta_disponible(self, dia):
        return normalizar_texto(dia) in self._dias_disponibles

    def contar_platos(self):
        return 1


class Bebida(Producto):
    """Bebida cuyo precio base corresponde a un vaso."""

    PRESENTACIONES = {"vaso", "jarra"}

    def __init__(self, nombre, precio, tipo, presentacion="vaso"):
        super().__init__(nombre, precio)
        self.tipo = tipo
        self.presentacion = presentacion

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tipo de bebida no puede estar vacío")
        self._tipo = valor.strip()

    @property
    def presentacion(self):
        return self._presentacion

    @presentacion.setter
    def presentacion(self, valor):
        presentacion = normalizar_texto(valor)
        if presentacion not in self.PRESENTACIONES:
            raise ValueError("La presentación debe ser vaso o jarra")
        self._presentacion = presentacion

    def calcular_precio(self):
        if self.presentacion == "jarra":
            return round(self.precio * 3, 2)
        return self.precio

    def esta_disponible(self, dia):
        return normalizar_texto(dia) in DIAS_VALIDOS

    def contar_platos(self):
        return 0


class Combo(Producto):
    """Producto compuesto con descuento del 10 % para la variante A."""

    DESCUENTO_VARIANTE_A = 0.10

    def __init__(self, nombre, productos):
        self._productos = []
        productos_iniciales = list(productos)
        if len(productos_iniciales) < 2:
            raise ValueError("Un combo debe contener al menos dos productos")
        for producto in productos_iniciales:
            self._validar_producto(producto)
            self._productos.append(producto)

        precio_inicial = self._calcular_precio_actual()
        super().__init__(nombre, precio_inicial)

    @property
    def productos(self):
        # Se entrega una tupla para impedir modificaciones externas.
        return tuple(self._productos)

    @property
    def descuento(self):
        return self.DESCUENTO_VARIANTE_A

    def _validar_producto(self, producto):
        try:
            produce_ciclo = producto.contiene(self)
            producto.calcular_precio()
            producto.esta_disponible("lunes")
            producto.contar_platos()
        except AttributeError as error:
            raise TypeError("Un combo solo puede contener productos") from error
        if produce_ciclo:
            raise ValueError("Un combo no puede contenerse a sí mismo ni formar ciclos")

    def _calcular_precio_actual(self):
        subtotal = sum(producto.calcular_precio() for producto in self._productos)
        return round(subtotal * (1 - self.DESCUENTO_VARIANTE_A), 2)

    def calcular_descuento(self):
        subtotal = sum(producto.calcular_precio() for producto in self._productos)
        descuento_propio = round(subtotal * self.DESCUENTO_VARIANTE_A, 2)
        descuentos_internos = sum(
            producto.calcular_descuento() for producto in self._productos
        )
        return round(descuento_propio + descuentos_internos, 2)

    def agregar_producto(self, producto):
        self._validar_producto(producto)
        self._productos.append(producto)
        self.precio = self._calcular_precio_actual()

    def quitar_producto(self, producto):
        if producto not in self._productos:
            raise ValueError("El producto no pertenece al combo")
        if len(self._productos) <= 2:
            raise ValueError("El combo debe conservar al menos dos productos")
        self._productos.remove(producto)
        self.precio = self._calcular_precio_actual()

    def contiene(self, producto_buscado):
        if self is producto_buscado:
            return True
        return any(
            producto.contiene(producto_buscado) for producto in self._productos
        )

    def calcular_precio(self):
        self.precio = self._calcular_precio_actual()
        return self.precio

    def esta_disponible(self, dia):
        return all(producto.esta_disponible(dia) for producto in self._productos)

    def contar_platos(self):
        return sum(producto.contar_platos() for producto in self._productos)

