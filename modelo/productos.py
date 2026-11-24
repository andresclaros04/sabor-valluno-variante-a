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

    def _contiene(self, producto_buscado):
        """Permite detectar ciclos sin preguntar por el tipo concreto."""
        return self is producto_buscado

    def _calcular_descuento(self):
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


class ComboProducto:
    """Clase asociativa entre un combo y cada producto que lo compone."""

    def __init__(self, combo, producto):
        self._combo = combo
        self._producto = producto

    @property
    def combo(self):
        return self._combo

    @property
    def producto(self):
        return self._producto


class Combo(Producto):
    """Producto compuesto con descuento del 10 % para la variante A."""

    DESCUENTO_VARIANTE_A = 0.10

    def __init__(self, nombre, productos):
        self._descuento = self.DESCUENTO_VARIANTE_A
        self._productos = []
        productos_iniciales = list(productos)
        if len(productos_iniciales) < 2:
            raise ValueError("Un combo debe contener al menos dos productos")
        for producto in productos_iniciales:
            self._validar_producto(producto)
            self._productos.append(ComboProducto(self, producto))

        precio_inicial = self._calcular_precio_actual()
        super().__init__(nombre, precio_inicial)

    @property
    def productos(self):
        # La relación se mantiene encapsulada y se exponen los productos.
        return tuple(relacion.producto for relacion in self._productos)

    @property
    def relaciones_productos(self):
        return tuple(self._productos)

    @property
    def descuento(self):
        return self._descuento

    def _validar_producto(self, producto):
        try:
            produce_ciclo = producto._contiene(self)
            producto.calcular_precio()
            producto.esta_disponible("lunes")
            producto.contar_platos()
        except AttributeError as error:
            raise TypeError("Un combo solo puede contener productos") from error
        if produce_ciclo:
            raise ValueError("Un combo no puede contenerse a sí mismo ni formar ciclos")

    def _calcular_precio_actual(self):
        subtotal = sum(producto.calcular_precio() for producto in self.productos)
        return round(subtotal * (1 - self.descuento), 2)

    def calcular_descuento(self):
        subtotal = sum(producto.calcular_precio() for producto in self.productos)
        descuento_propio = round(subtotal * self.descuento, 2)
        descuentos_internos = sum(
            producto._calcular_descuento() for producto in self.productos
        )
        return round(descuento_propio + descuentos_internos, 2)

    def _calcular_descuento(self):
        return self.calcular_descuento()

    def _contiene(self, producto_buscado):
        if self is producto_buscado:
            return True
        return any(
            producto._contiene(producto_buscado) for producto in self.productos
        )

    def calcular_precio(self):
        self.precio = self._calcular_precio_actual()
        return self.precio

    def esta_disponible(self, dia):
        return all(producto.esta_disponible(dia) for producto in self.productos)

    def contar_platos(self):
        return sum(producto.contar_platos() for producto in self.productos)

