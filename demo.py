"""Demostración automática del caso de referencia de la variante A."""

from datetime import datetime

from modelo.clientes import Cliente
from modelo.pagos import PagoQR
from modelo.pedidos import PedidoDelivery
from modelo.productos import Bebida, Combo, Plato
from restaurante import Restaurante


def ejecutar_demo():
    restaurante = Restaurante()

    silpancho = Plato("Silpancho", 35)
    mocochinchi = Bebida("Mocochinchi", 6, "refresco natural", "vaso")
    combo = Combo("Combo silpancho", [silpancho, mocochinchi])

    restaurante.registrar_producto(silpancho)
    restaurante.registrar_producto(mocochinchi)
    restaurante.registrar_producto(combo)

    cliente = Cliente("Cliente demostración", "71234567")
    restaurante.registrar_cliente(cliente)

    pedido = PedidoDelivery(
        1,
        cliente,
        "Quillacollo",
        datetime(2026, 11, 23, 12, 0),
    )
    pedido.agregar_producto(combo, 2)
    restaurante.registrar_pedido(pedido)

    detalle = pedido.detalle()
    print("=== CASO DE REFERENCIA VARIANTE A ===")
    print(f"Combo individual: Bs {combo.calcular_precio():.2f}")
    print(f"Subtotal bruto: Bs {detalle['subtotal_bruto']:.2f}")
    print(f"Descuentos: Bs {detalle['descuentos']:.2f}")
    print(f"Subtotal con descuento: Bs {detalle['subtotal']:.2f}")
    print(f"Envío a Quillacollo: Bs {detalle['cargos']:.2f}")
    print(f"Total: Bs {detalle['total']:.2f}")

    comprobante = pedido.cobrar(PagoQR("1234567890"))
    print("\n=== COMPROBANTE ===")
    for clave, valor in comprobante.items():
        print(f"{clave}: {valor}")

    reporte = restaurante.reporte_ventas(pedido.fecha_registro.date())
    print("\n=== REPORTE ===")
    print(f"Pedidos delivery: {reporte['cantidad_por_tipo']['DELIVERY']}")
    print(f"Total de ventas: Bs {reporte['total_general']:.2f}")
    print(f"Más vendido: {reporte['productos_mas_vendidos'][0]}")


if __name__ == "__main__":
    ejecutar_demo()

