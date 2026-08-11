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


def nombre_herramienta(id_herramienta):
    herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
    return herramienta["nombre"] if herramienta else "Desconocida"


def nombre_usuario(id_usuario):
    usuario = mod_usuarios.buscar_usuario(id_usuario)
    if usuario:
        return usuario["nombres"] + " " + usuario["apellidos"]
    return "Desconocido"


def menu_administrador():
    print("\n--- MENU ADMINISTRADOR ---")
    print("1. Registrar Herramienta")
    print("2. Listar Herramientas")
    print("3. Registrar Vecino")
    print("4. Listar Vecinos")
    print("5. Aprobar solicitud de prestamo")
    print("6. Registrar Devolucion")
    print("7. Ver Reportes")
    print("8. Actualizar Vecino")
    print("9. Volver")


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
            nueva = mod_herramientas.crear_herramienta(nombre, categoria, cantidad, valor)
            print("Herramienta Registrada con ID", nueva["id"], "-", nueva["nombre"])

        elif opcion == "2":
            print("\nID  NOMBRE               DISPONIBLE  ESTADO")
            for h in mod_herramientas.listar_herramientas():
                print(h["id"], "-", h["nombre"], "-",
                      h["cantidad_disponible"], "disp. -", h["estado"])

        elif opcion == "3":
            nombres = input("Nombres: ").strip()
            apellidos = input("Apellidos: ").strip()
            telefono = input("Telefono: ").strip()
            direccion = input("Direccion: ").strip()
            nuevo = mod_usuarios.crear_usuario(nombres, apellidos, telefono, direccion, "residente")
            print("Vecino Registrado con ID", nuevo["id"], "-", nuevo["nombres"], nuevo["apellidos"])

        elif opcion == "4":
            print("\nID  NOMBRE COMPLETO          TELEFONO")
            for u in mod_usuarios.listar_usuarios():
                print(u["id"], "-", u["nombres"], u["apellidos"], "-", u["telefono"])

        elif opcion == "5":
            pendientes = [p for p in mod_prestamos.listar_prestamos() if p["estado"] == "pendiente"]
            if not pendientes:
                print("No hay solicitudes pendientes.")
            else:
                for p in pendientes:
                    print("Prestamo", p["id"], "-", nombre_usuario(p["id_usuario"]),
                          "solicita", p["cantidad"], "x", nombre_herramienta(p["id_herramienta"]))
                id_prestamo = pedir_numero_entero("\nId del prestamo a procesar: ")
                decision = input("¿Aprobar o Rechazar? (A/R): ").strip().upper()
                if decision == "A":
                    if mod_prestamos.aprobar_prestamo(id_prestamo):
                        print("Prestamo Aprobado.")
                    else:
                        print("No se pudo aprobar (sin stock suficiente o id invalido). Revisa el log.")
                elif decision == "R":
                    motivo = input("Motivo del rechazo (opcional): ").strip()
                    if mod_prestamos.rechazar_prestamo(id_prestamo, motivo):
                        print("Prestamo Rechazado.")
                    else:
                        print("No se pudo rechazar. Revisa que el id sea correcto.")
                else:
                    print("Opcion invalida. No se realizo ningun cambio.")

        elif opcion == "6":
            activos = [p for p in mod_prestamos.listar_prestamos() if p["estado"] == "activo"]
            if not activos:
                print("No hay prestamos activos.")
            for p in activos:
                print("Prestamo", p["id"], "-", nombre_usuario(p["id_usuario"]),
                      "tiene", p["cantidad"], "x", nombre_herramienta(p["id_herramienta"]))
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
                print("Prestamo", p["id"], "-", nombre_usuario(p["id_usuario"]), "-",
                      nombre_herramienta(p["id_herramienta"]), "- vence el", p["fecha_devolucion_estimada"])

            print("\n-- Prestamos vencidos --")
            for p in mod_reportes.prestamos_vencidos():
                print("Prestamo", p["id"], "-", nombre_usuario(p["id_usuario"]), "-",
                      nombre_herramienta(p["id_herramienta"]), "- vencio el", p["fecha_devolucion_estimada"])

            print("\n-- Herramientas mas solicitadas --")
            for item in mod_reportes.herramientas_mas_solicitadas():
                print(item["nombre"], "-", item["veces"], "vez(ces)")

            print("\n-- Vecinos que mas solicitan --")
            for item in mod_reportes.usuarios_mas_solicitantes():
                print(item["nombre"], "-", item["veces"], "vez(ces)")

        elif opcion == "8":
            print("\nVecinos registrados:")
            for u in mod_usuarios.listar_usuarios():
                print(u["id"], "-", u["nombres"], u["apellidos"], "-", u["telefono"])
            id_usuario = pedir_numero_entero("\nId del vecino a actualizar: ")
            print("¿Qué dato deseas actualizar?")
            print("1. Telefono")
            print("2. Direccion")
            campo_opcion = input("Opcion: ").strip()
            if campo_opcion == "1":
                nuevo_valor = input("Nuevo telefono: ").strip()
                if mod_usuarios.actualizar_usuario(id_usuario, "telefono", nuevo_valor):
                    print("Telefono actualizado correctamente.")
                else:
                    print("No se pudo actualizar. Verifica el id.")
            elif campo_opcion == "2":
                nuevo_valor = input("Nueva direccion: ").strip()
                if mod_usuarios.actualizar_usuario(id_usuario, "direccion", nuevo_valor):
                    print("Direccion actualizada correctamente.")
                else:
                    print("No se pudo actualizar. Verifica el id.")
            else:
                print("Opcion invalida.")

        elif opcion == "9":
            break
        else:
            print("Opcion invalida.")


def opciones_usuario():
    print("\nVecinos registrados:")
    print("ID  NOMBRE COMPLETO")
    for u in mod_usuarios.listar_usuarios():
        print(u["id"], "-", u["nombres"], u["apellidos"])
    id_usuario = pedir_numero_entero("\nIngresa tu id de vecino: ")
    print("Hola,", nombre_usuario(id_usuario))
    while True:
        menu_usuario()
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            print("\nID  NOMBRE               DISPONIBLE")
            for h in mod_herramientas.listar_herramientas():
                if h["estado"] == "activa":
                    print(h["id"], "-", h["nombre"], "-",
                          h["cantidad_disponible"], "disponible(s)")

        elif opcion == "2":
            print("\nHerramientas disponibles:")
            print("ID  NOMBRE               DISPONIBLE")
            for h in mod_herramientas.listar_herramientas():
                if h["estado"] == "activa" and h["cantidad_disponible"] > 0:
                    print(h["id"], "-", h["nombre"], "-",
                          h["cantidad_disponible"], "disponible(s)")
            id_herramienta = pedir_numero_entero("\nId de la herramienta: ")
            cantidad = pedir_numero_entero("Cantidad: ")
            observaciones = input("Observaciones: ").strip()

            herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
            if herramienta and cantidad > herramienta["cantidad_disponible"]:
                print("Aviso: pediste", cantidad, "unidades, pero ahora mismo solo hay",
                      herramienta["cantidad_disponible"], "disponibles. La solicitud se enviara",
                      "de todas formas, pero es probable que el administrador la rechace a menos",
                      "que el stock cambie antes de que la revise.")

            solicitud = mod_prestamos.solicitar_prestamo(
                id_usuario, id_herramienta, cantidad, observaciones)
            if solicitud:
                print("Solicitud creada con ID", solicitud["id"], "-", nombre_usuario(id_usuario),
                      "solicita", cantidad, "x", nombre_herramienta(id_herramienta), "- espera aprobacion.")
            else:
                print("No se pudo crear la solicitud.")

        elif opcion == "3":
            for p in mod_prestamos.listar_prestamos():
                if p["id_usuario"] == id_usuario:
                    print("Prestamo", p["id"], "-", nombre_herramienta(p["id_herramienta"]),
                          "-", p["cantidad"], "unidad(es) -", p["estado"])

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