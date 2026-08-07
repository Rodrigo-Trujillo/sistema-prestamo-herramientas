import herramientas as mod_herramientas
import usuarios as mod_usuarios
import prestamos as mod_prestamos
import reportes as mod_reportes


def pedir_numero_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debes ingresar un numero entero")


def menu_administrador():
    print("\n--- MENU ADMINISTRADOR ---")
    print("1. Registrar Herramienta")
    print("2. Listar Herramientas")
    print("3. Registrar Vecino")
    print("4. Listar Vecinos")
    print("5. Aprobar solicitud de prestamo")
    print("6. Registrar Devolucion")
    print("7. Ver Reportes")
    print("8. Volver")


def menu_usuario():
    print("\n--- MENU VECINO ---")
    print("1. Ver Herramientas Disponibles")
    print("2. Solicitar Prestamo")
    print("3. Ver Mi Historial")
    print("4. Volver")


def opciones_administrador():
    while True:
        menu_administrador()
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            nombre = input("Nombre: ").strip()
            categoria = input("Categoria: ").strip()
            cantidad = pedir_numero_entero("Cantidad: ")
            valor = pedir_numero_entero("Valor Estimado: ")
            mod_herramientas.crear_herramienta(nombre, categoria, cantidad, valor)
            print("Herramienta Registrada.")
        elif opcion == "2":
            for h in mod_herramientas.listar_herramientas():
                print(h["id"], "-", h["nombre"], "-",
                      h["cantidad_disponible"], "disp. -", h["estado"])
        elif opcion == "5":
            for p in mod_prestamos.listar_prestamos():
                if p["estado"] == "pendiente":
                    print("Prestamo", p["id"], "- usuario", p["id_usuario"])
            id_prestamo = pedir_numero_entero("Id prestamo a aprobar: ")
            if mod_prestamos.aprobar_prestamo(id_prestamo):
                print("Prestamo Aprobado.")
            else:
                print("No se pudo aprobar. Revisa el log.")
        elif opcion == "8":
            break
        else:
            print("Opcion invalida.")


def main():
    print("=== SISTEMA DE PRESTAMOS DE HERRAMIENTAS ===")
    while True:
        print("\n1. Entrar Como Administrador")
        print("\n2. Entrar Como Vecino")
        print("\n3. Salir")
        rol = input("Opcion: ").strip()
        if rol == "1":
            opciones_administrador()
        elif rol == "2":
            opciones_usuario()
        elif rol == "3":
            print("Hasta Luego.")
            break
        else:
            print("Opcion Invalida.")


if __name__ == "__main__":
    main()