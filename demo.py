"""Demostración automática del caso de referencia de la variante A."""

from datetime import datetime

from modelo.clientes import Cliente
from modelo.pagos import QR
from modelo.pedidos import Delivery
from modelo.productos import Bebida, Combo, Plato
import restaurante as servicio


def ejecutar_demo():
    restaurante = servicio.crear_sistema()

    silpancho = Plato("Silpancho", 35)
    mocochinchi = Bebida("Mocochinchi", 6, "refresco natural", "vaso")
    combo = Combo("Combo silpancho", [silpancho, mocochinchi])

    servicio.registrar_producto(restaurante, silpancho)
    servicio.registrar_producto(restaurante, mocochinchi)
    servicio.registrar_producto(restaurante, combo)

    cliente = Cliente("Cliente demostración", "71234567")
    servicio.registrar_cliente(restaurante, cliente)

    pedido = Delivery(
        1,
        cliente,
        "Quillacollo",
        datetime(2026, 11, 23, 12, 0),
    )
    pedido.agregar_producto(combo, 2)
    servicio.registrar_pedido(restaurante, pedido)

    detalle = pedido.detalle()
    print("=== CASO DE REFERENCIA VARIANTE A ===")
    print(f"Combo individual: Bs {combo.calcular_precio():.2f}")
    print(f"Subtotal bruto: Bs {detalle['subtotal_bruto']:.2f}")
    print(f"Descuentos: Bs {detalle['descuentos']:.2f}")
    print(f"Subtotal con descuento: Bs {detalle['subtotal']:.2f}")
    print(f"Envío a Quillacollo: Bs {detalle['cargos']:.2f}")
    print(f"Total: Bs {detalle['total']:.2f}")

    comprobante = pedido.cobrar(QR("1234567890"))
    print("\n=== COMPROBANTE ===")
    for clave, valor in comprobante.items():
        print(f"{clave}: {valor}")

    reporte = servicio.reporte_ventas(restaurante, pedido.fecha_registro.date())
    print("\n=== REPORTE ===")
    print(f"Pedidos delivery: {reporte['cantidad_por_tipo']['DELIVERY']}")
    print(f"Total de ventas: Bs {reporte['total_general']:.2f}")
    print(f"Más vendido: {reporte['productos_mas_vendidos'][0]}")


if __name__ == "__main__":
    ejecutar_demo()

