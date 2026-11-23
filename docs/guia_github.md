# Guía para publicar el proyecto en GitHub

El repositorio local ya está inicializado y contiene los commits del proyecto. No se debe crear otro repositorio dentro de esta carpeta.

## Opción 1 Publicar desde VS Code

1. Abrir únicamente la carpeta `sabor_valluno` en VS Code.
2. Abrir el panel **Control de código fuente**.
3. Comprobar que aparezca el historial del proyecto y que no haya cambios pendientes.
4. Seleccionar **Publish Branch** o **Publicar rama**.
5. Iniciar sesión en la cuenta personal de GitHub.
6. Escribir el nombre `sabor-valluno-variante-a`.
7. Elegir repositorio privado o público según la indicación del docente.
8. Esperar a que VS Code confirme la publicación.
9. Abrir el repositorio desde el navegador y comprobar que estén `README.md`, `main.py`, `pruebas.py`, `modelo/` y `docs/`.
10. Copiar el enlace del repositorio para la entrega.

## Opción 2 Publicar desde la terminal

Primero se crea en GitHub un repositorio vacío llamado `sabor-valluno-variante-a`. No se debe agregar README, `.gitignore` ni licencia desde la página, porque esos archivos ya existen localmente.

Después, dentro de la carpeta `sabor_valluno`, se ejecuta:

```text
git branch -M main
git remote add origin https://github.com/USUARIO/sabor-valluno-variante-a.git
git push -u origin main
```

Se debe reemplazar `USUARIO` por el nombre real de la cuenta.

## Verificación

Ejecutar:

```text
git remote -v
git status
git log --oneline
```

El resultado esperado es:

- `origin` apunta al repositorio correcto.
- La rama local está sincronizada con `origin/main`.
- No existen cambios pendientes.
- El historial conserva todos los commits realizados.

## Seguridad

- No escribir contraseñas o tokens dentro del código.
- No compartir capturas que muestren credenciales.
- No subir `datos.json` con información personal real.
- No borrar la bitácora de IA antes de entregar.
- Si el repositorio es público, revisar especialmente nombres, teléfonos y archivos temporales.

