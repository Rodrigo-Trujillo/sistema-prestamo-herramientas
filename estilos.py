"""
Modulo de estilos: colores, emojis y elementos visuales para la consola.
Centraliza toda la presentacion para que main.py quede limpio.
"""
import os

# Activa los colores ANSI en la consola de Windows
os.system("")

# --- COLORES ---
RESET = "\033[0m"
NEGRITA = "\033[1m"

ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CIAN = "\033[96m"
GRIS = "\033[90m"

ANCHO = 52


def titulo(texto):
    """Encabezado principal del programa."""
    print()
    print(CIAN + NEGRITA + "=" * ANCHO + RESET)
    print(CIAN + NEGRITA + texto.center(ANCHO) + RESET)
    print(CIAN + NEGRITA + "=" * ANCHO + RESET)


def seccion(texto):
    """Encabezado de un menu o seccion."""
    print()
    print(AZUL + NEGRITA + "-" * ANCHO + RESET)
    print(AZUL + NEGRITA + texto.center(ANCHO) + RESET)
    print(AZUL + NEGRITA + "-" * ANCHO + RESET)


def opcion(numero, emoji, texto):
    """Una linea del menu."""
    print("  " + AMARILLO + NEGRITA + str(numero) + "." + RESET + " " + emoji + "  " + texto)


def exito(texto):
    print(VERDE + "[OK] " + texto + RESET)


def error(texto):
    print(ROJO + "[X] " + texto + RESET)


def aviso(texto):
    print(AMARILLO + "[!] " + texto + RESET)


def info(texto):
    print(CIAN + "[i] " + texto + RESET)


def subtitulo(texto):
    print()
    print(MAGENTA + NEGRITA + ">> " + texto + RESET)


def linea():
    print(GRIS + "-" * ANCHO + RESET)


def item(texto):
    print("   " + texto)


def despedida(texto):
    print()
    print(CIAN + NEGRITA + texto.center(ANCHO) + RESET)
    print()
