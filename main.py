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
        elif opcion == "3":
            nombres = input("Nombres: ").strip()
            apellidos = input("Apellidos: ").strip()
            telefono = input("Telefono: ").strip()
            direccion = input("Direccion: ").strip()
            mod_usuarios.crear_usuario(nombres, apellidos, telefono, direccion, "residente")
            print("Vecino Registrado.")
        elif opcion == "4":
            for u in mod_usuarios.listar_usuarios():
                print(u["id"], "-", u["nombres"], u["apellidos"], "-", u["telefono"])
        elif opcion == "5":
            for p in mod_prestamos.listar_prestamos():
                if p["estado"] == "pendiente":
                    print("Prestamo", p["id"], "- usuario", p["id_usuario"])
            id_prestamo = pedir_numero_entero("Id prestamo a aprobar: ")
            if mod_prestamos.aprobar_prestamo(id_prestamo):
                print("Prestamo Aprobado.")
            else:
                print("No se pudo aprobar. Revisa el log.")
        elif opcion == "6":
            id_prestamo = pedir_numero_entero("Id prestamo devuelto: ")
            if mod_prestamos.devolver_prestamo(id_prestamo):
                print("Devolucion registrada.")
            else:
                print("No se pudo registrar la devolucion.")
        elif opcion == "7":
            print("\n-- Herramientas con stock bajo --")
            for h in mod_reportes.stock_bajo():
                print(h["nombre"], "-", h["cantidad_disponible"], "unidad(es)")

            print("\n-- Prestamos activos --")
            for p in mod_reportes.prestamos_activos():
                print("Prestamo", p["id"], "- vence el", p["fecha_devolucion_estimada"])

            print("\n-- Prestamos vencidos --")
            for p in mod_reportes.prestamos_vencidos():
                print("Prestamo", p["id"], "- vencio el", p["fecha_devolucion_estimada"])

            print("\n-- Herramientas mas solicitadas --")
            for item in mod_reportes.herramientas_mas_solicitadas():
                print(item["nombre"], "-", item["veces"], "vez(ces)")

            print("\n-- Vecinos que mas solicitan --")
            for item in mod_reportes.usuarios_mas_solicitantes():
                print(item["nombre"], "-", item["veces"], "vez(ces)")
        elif opcion == "8":
            break
        else:
            print("Opcion invalida.")


def opciones_usuario():
    id_usuario = pedir_numero_entero("Ingresa tu id de vecino: ")
    while True:
        menu_usuario()
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            for h in mod_herramientas.listar_herramientas():
                if h["estado"] == "activa":
                    print(h["id"], "-", h["nombre"], "-",
                          h["cantidad_disponible"], "disponible(s)")
        elif opcion == "2":
            id_herramienta = pedir_numero_entero("Id de la herramienta: ")
            cantidad = pedir_numero_entero("Cantidad: ")
            observaciones = input("Observaciones: ").strip()
            solicitud = mod_prestamos.solicitar_prestamo(
                id_usuario, id_herramienta, cantidad, observaciones)
            if solicitud:
                print("Solicitud creada con id", solicitud["id"], "- espera aprobacion.")
            else:
                print("No se pudo crear la solicitud.")
        elif opcion == "3":
            for p in mod_prestamos.listar_prestamos():
                if p["id_usuario"] == id_usuario:
                    print("Prestamo", p["id"], "- herramienta", p["id_herramienta"], "-", p["estado"])
        elif opcion == "4":
            break
        else:
            print("Opcion invalida.")


def main():
    print("=== SISTEMA DE PRESTAMOS DE HERRAMIENTAS ===")
    while True:
        print("\n1. Entrar Como Administrador")
        print("2. Entrar Como Vecino")
        print("3. Salir")
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