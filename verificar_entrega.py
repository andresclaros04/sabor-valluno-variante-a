"""Verificación rápida de la estructura y comportamiento antes de entregar."""

from pathlib import Path

import pruebas


RAIZ = Path(__file__).resolve().parent

ARCHIVOS_REQUERIDOS = (
    "modelo/__init__.py",
    "modelo/productos.py",
    "modelo/clientes.py",
    "modelo/pedidos.py",
    "modelo/pagos.py",
    "restaurante.py",
    "main.py",
    "pruebas.py",
    "README.md",
    "docs/diagrama_v1.png",
    "docs/diagrama_v2.png",
    "docs/bitacora_ia.md",
    "docs/acta_consultas.md",
    "docs/registro_ia_claros.md",
)


def verificar_archivos():
    faltantes = [
        ruta for ruta in ARCHIVOS_REQUERIDOS if not (RAIZ / ruta).is_file()
    ]
    if faltantes:
        raise AssertionError(
            "Faltan archivos requeridos: " + ", ".join(faltantes)
        )
    print(f"[OK] {len(ARCHIVOS_REQUERIDOS)} archivos requeridos")


def ejecutar_pruebas():
    if len(pruebas.PRUEBAS) < 8:
        raise AssertionError("La consigna exige al menos 8 casos de prueba")
    for prueba in pruebas.PRUEBAS:
        prueba()
    print(f"[OK] {len(pruebas.PRUEBAS)} pruebas funcionales")


def revisar_pendientes_documentales():
    acta = (RAIZ / "docs/acta_consultas.md").read_text(encoding="utf-8")
    cantidad = acta.lower().count("pendiente")
    if cantidad:
        print(
            f"[AVISO] El acta todavía contiene {cantidad} campos pendientes"
        )
    else:
        print("[OK] Acta sin campos pendientes")


def ejecutar():
    print("Verificación del proyecto Sabor Valluno variante A")
    verificar_archivos()
    ejecutar_pruebas()
    revisar_pendientes_documentales()
    print("Verificación técnica terminada")


if __name__ == "__main__":
    ejecutar()

