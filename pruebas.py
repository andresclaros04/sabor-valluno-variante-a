"""Pruebas ejecutables del sistema Sabor Valluno: ``python pruebas.py``."""

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from modelo.clientes import Cliente
from modelo.pagos import Efectivo, MetodoPago, QR, Tarjeta
from modelo.pedidos import Delivery, Local, ParaLlevar, Pedido
from modelo.productos import Bebida, Combo, ComboProducto, Plato, Producto
from persistencia import cargar_json, guardar_json
import restaurante as servicio


def verificar_excepcion(tipo_excepcion, funcion):
    try:
        funcion()
    except tipo_excepcion:
        return
    raise AssertionError(f"Se esperaba {tipo_excepcion.__name__}")


def crear_productos_referencia():
    plato = Plato("Silpancho", 35)
    bebida = Bebida("Mocochinchi", 6, "refresco natural", "vaso")
    combo = Combo("Combo silpancho", [plato, bebida])
    return plato, bebida, combo


def probar_clases_abstractas():
    cliente = Cliente("Ana", "71234567")
    verificar_excepcion(TypeError, lambda: Producto("Genérico", 10))
    verificar_excepcion(TypeError, lambda: Pedido(1, cliente))
    verificar_excepcion(TypeError, MetodoPago)


def probar_plato_y_chicharron():
    verificar_excepcion(ValueError, lambda: Plato("Silpancho", 0))
    chicharron = Plato("Chicharrón", 45)
    assert not chicharron.esta_disponible("sábado")
    assert chicharron.esta_disponible("domingo")
    assert chicharron.contar_platos() == 1


def probar_bebida_vaso_y_jarra():
    bebida = Bebida("Mocochinchi", 6, "natural", "vaso")
    assert bebida.calcular_precio() == 6
    bebida.presentacion = "jarra"
    assert bebida.calcular_precio() == 18
    assert bebida.contar_platos() == 0


def probar_combo_y_clase_asociativa():
    plato, bebida, combo = crear_productos_referencia()
    assert combo.calcular_precio() == 36.90
    assert combo.calcular_descuento() == 4.10
    assert combo.contar_platos() == 1
    assert len(combo.relaciones_productos) == 2
    assert all(isinstance(item, ComboProducto) for item in combo.relaciones_productos)
    assert combo.relaciones_productos[0].combo is combo
    assert combo.productos == (plato, bebida)


def probar_combo_anidado_y_envases():
    plato, _, combo = crear_productos_referencia()
    anidado = Combo("Combo doble", [combo, plato])
    assert anidado.contar_platos() == 2
    pedido = ParaLlevar(1, Cliente("Ana", "71234567"))
    pedido.agregar_producto(anidado, 2)
    assert pedido.calcular_cargos() == 8.0


def probar_caso_referencia_88_80():
    _, _, combo = crear_productos_referencia()
    pedido = Delivery(
        1, Cliente("Luis", "61234567"), "Quillacollo",
        datetime(2026, 11, 23, 12, 0),
    )
    pedido.agregar_producto(combo, 2)
    assert pedido.detalle()["subtotal_bruto"] == 82.00
    assert pedido.detalle()["descuentos"] == 8.20
    assert pedido.calcular_subtotal() == 73.80
    assert pedido.calcular_cargos() == 15.0
    assert pedido.calcular_total() == 88.80


def probar_cantidades_y_estados():
    plato, _, _ = crear_productos_referencia()
    pedido = Local(1, Cliente("Rosa", "72345678"), 5)
    verificar_excepcion(ValueError, lambda: pedido.cambiar_estado(Pedido.EN_PREPARACION))
    pedido.agregar_producto(plato, 1)
    verificar_excepcion(ValueError, lambda: pedido.agregar_producto(plato, -1))
    assert pedido.items[0].cantidad == 1
    pedido.cambiar_estado(Pedido.EN_PREPARACION)
    verificar_excepcion(ValueError, lambda: pedido.agregar_producto(plato, 1))
    verificar_excepcion(ValueError, lambda: pedido.cambiar_estado(Pedido.ENTREGADO))


def probar_reglas_delivery():
    plato, _, _ = crear_productos_referencia()
    cliente = Cliente("Eva", "73456789")
    pequeno = Delivery(1, cliente, "Cercado")
    pequeno.agregar_producto(plato, 1)
    verificar_excepcion(ValueError, lambda: pequeno.cambiar_estado(Pedido.EN_PREPARACION))
    verificar_excepcion(ValueError, lambda: pequeno.cobrar(QR("0987654321")))
    gratis = Delivery(2, cliente, "Cercado")
    gratis.agregar_producto(plato, 5)
    assert gratis.calcular_cargos() == 0.0
    verificar_excepcion(ValueError, lambda: gratis.cobrar(Tarjeta()))


def probar_metodos_pago():
    plato, _, _ = crear_productos_referencia()
    cliente = Cliente("Mario", "74567890")
    efectivo = Local(1, cliente, 1)
    efectivo.agregar_producto(plato)
    comprobante = efectivo.cobrar(Efectivo(40))
    assert comprobante["cambio"] == 5.0
    verificar_excepcion(ValueError, efectivo.cancelar)
    verificar_excepcion(ValueError, lambda: efectivo.cobrar(Efectivo(40)))
    tarjeta = Local(2, cliente, 2)
    tarjeta.agregar_producto(plato)
    comprobante = tarjeta.cobrar(Tarjeta())
    assert comprobante["comision"] == 1.05
    assert comprobante["total"] == 36.05
    verificar_excepcion(ValueError, lambda: QR("123"))


def probar_ocupacion_de_mesas():
    restaurante = servicio.crear_sistema()
    cliente = Cliente("Sonia", "75678901")
    servicio.registrar_cliente(restaurante, cliente)
    servicio.registrar_pedido(restaurante, Local(1, cliente, 3))
    assert not servicio.mesa_disponible(restaurante, 3)
    verificar_excepcion(
        ValueError,
        lambda: servicio.registrar_pedido(restaurante, Local(2, cliente, 3)),
    )


def probar_reporte_diario():
    restaurante = servicio.crear_sistema()
    cliente = Cliente("Nora", "76789012")
    plato, bebida, combo = crear_productos_referencia()
    for producto in (plato, bebida, combo):
        servicio.registrar_producto(restaurante, producto)
    servicio.registrar_cliente(restaurante, cliente)
    pedido = Local(1, cliente, 1)
    pedido.agregar_producto(combo, 2)
    pedido.cobrar(Efectivo(100))
    servicio.registrar_pedido(restaurante, pedido)
    reporte = servicio.reporte_ventas(restaurante, pedido.fecha_registro.date())
    assert reporte["cantidad_por_tipo"]["LOCAL"] == 1
    assert reporte["total_general"] == 73.80
    assert reporte["productos_mas_vendidos"] == [("Combo silpancho", 2)]


def probar_persistencia_json_con_combo_anidado():
    restaurante = servicio.crear_sistema()
    cliente = Cliente("Pablo", "77890123")
    plato, bebida, combo = crear_productos_referencia()
    anidado = Combo("Combo familiar", [combo, plato])
    for producto in (plato, bebida, combo, anidado):
        servicio.registrar_producto(restaurante, producto)
    servicio.registrar_cliente(restaurante, cliente)
    pedido = Delivery(1, cliente, "Quillacollo")
    pedido.agregar_producto(anidado)
    pedido.cobrar(QR("1122334455"))
    servicio.registrar_pedido(restaurante, pedido)
    with TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "datos.json"
        guardar_json(restaurante, ruta)
        cargado = cargar_json(ruta)
    assert len(cargado["productos"]) == 4
    assert cargado["pedidos"][0].pago.nombre == "QR"
    assert cargado["pedidos"][0].items[0].producto.contar_platos() == 2


PRUEBAS = (
    probar_clases_abstractas,
    probar_plato_y_chicharron,
    probar_bebida_vaso_y_jarra,
    probar_combo_y_clase_asociativa,
    probar_combo_anidado_y_envases,
    probar_caso_referencia_88_80,
    probar_cantidades_y_estados,
    probar_reglas_delivery,
    probar_metodos_pago,
    probar_ocupacion_de_mesas,
    probar_reporte_diario,
    probar_persistencia_json_con_combo_anidado,
)


def ejecutar_todas():
    for prueba in PRUEBAS:
        prueba()
        print(f"[OK] {prueba.__name__}")
    print(f"Todas las pruebas superadas: {len(PRUEBAS)} casos")


if __name__ == "__main__":
    ejecutar_todas()
