"""Crea el ZIP final solamente cuando la documentación obligatoria está completa."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


RAIZ = Path(__file__).resolve().parent
ACTA = RAIZ / "docs" / "acta_consultas.md"
CARPETA_SALIDA = RAIZ / "entrega"
ARCHIVO_SALIDA = CARPETA_SALIDA / "Sabor_Valluno_Variante_A.zip"

CARPETAS_EXCLUIDAS = {".git", "__pycache__", "entrega"}
SUFIJOS_EXCLUIDOS = {".pyc", ".pyo"}
ARCHIVOS_EXCLUIDOS = {"datos.json"}


def validar_acta():
    contenido = ACTA.read_text(encoding="utf-8").lower()
    if "pendiente" in contenido:
        raise SystemExit(
            "No se creó el ZIP: complete primero los campos pendientes de "
            "docs/acta_consultas.md"
        )


def debe_incluir(ruta):
    if cualquier_parte_excluida(ruta):
        return False
    if ruta.suffix.lower() in SUFIJOS_EXCLUIDOS:
        return False
    if ruta.name in ARCHIVOS_EXCLUIDOS:
        return False
    return ruta.is_file()


def cualquier_parte_excluida(ruta):
    return any(parte in CARPETAS_EXCLUIDAS for parte in ruta.parts)


def crear_zip():
    validar_acta()
    CARPETA_SALIDA.mkdir(exist_ok=True)
    with ZipFile(ARCHIVO_SALIDA, "w", ZIP_DEFLATED) as archivo_zip:
        for ruta in RAIZ.rglob("*"):
            relativa = ruta.relative_to(RAIZ)
            if debe_incluir(relativa):
                archivo_zip.write(ruta, Path("sabor_valluno") / relativa)
    print(f"Paquete creado: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    crear_zip()

