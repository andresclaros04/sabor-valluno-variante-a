"""Clientes del restaurante Sabor Valluno."""


class Cliente:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        telefono = str(valor).strip()
        if len(telefono) != 8 or not telefono.isdigit():
            raise ValueError("El teléfono debe tener exactamente 8 dígitos")
        if telefono[0] not in {"6", "7"}:
            raise ValueError("El teléfono debe comenzar con 6 o 7")
        self._telefono = telefono

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"

