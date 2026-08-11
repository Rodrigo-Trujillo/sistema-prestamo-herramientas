import herramientas as mod_herramientas
import usuarios as mod_usuarios
import prestamos as mod_prestamos
import reportes as mod_reportes
import estilos as ui


def pedir_numero_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            ui.error("Debes ingresar un numero entero.")


def pedir_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        if telefono.isdigit() and len(telefono) == 10:
            return telefono
        ui.error("El telefono debe tener exactamente 10 digitos numericos.")


def nombre_herramienta(id_herramienta):
    herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
    return herramienta["nombre"] if herramienta else "Desconocida"


def nombre_usuario(id_usuario):
    usuario = mod_usuarios.buscar_usuario(id_usuario)
    if usuario:
        return usuario["nombres"] + " " + usuario["apellidos"]
    return "Desconocido"


def emoji_estado(estado):
    iconos = {
        "pendiente": "\u23f3",
        "activo": "\U0001f4e4",
        "devuelto": "\u2705",
        "rechazado": "\u274c",
        "activa": "\U0001f7e2",
        "en reparacion": "\U0001f527",
        "fuera de servicio": "\U0001f534",
    }
    return iconos.get(estado, "\u2022")


def mostrar_tabla_herramientas(solo_disponibles=False):
    herramientas = mod_herramientas.listar_herramientas()
    if solo_disponibles:
        herramientas = [h for h in herramientas
                        if h["estado"] == "activa" and h["cantidad_disponible"] > 0]
    if not herramientas:
        ui.aviso("No hay herramientas para mostrar.")
        return
    ui.linea()
    print("  ID   HERRAMIENTA          STOCK   ESTADO")
    ui.linea()
    for h in herramientas:
        print("  " + str(h["id"]).ljust(4) + " " + h["nombre"][:20].ljust(20) + " "
              + str(h["cantidad_disponible"]).center(5) + "   "
              + emoji_estado(h["estado"]) + " " + h["estado"])
    ui.linea()


def mostrar_tabla_vecinos():
    usuarios = mod_usuarios.listar_usuarios()
    if not usuarios:
        ui.aviso("No hay vecinos registrados.")
        return
    ui.linea()
    print("  ID   NOMBRE COMPLETO           TELEFONO")
    ui.linea()
    for u in usuarios:
        nombre = (u["nombres"] + " " + u["apellidos"])[:24]
        print("  " + str(u["id"]).ljust(4) + " " + nombre.ljust(25) + " " + u["telefono"])
    ui.linea()


def menu_administrador():
    ui.seccion("\U0001f6e0  MENU ADMINISTRADOR")
    ui.opcion(1, "\U0001f528", "Registrar Herramienta")
    ui.opcion(2, "\U0001f4cb", "Listar Herramientas")
    ui.opcion(3, "\U0001f464", "Registrar Vecino")
    ui.opcion(4, "\U0001f465", "Listar Vecinos")
    ui.opcion(5, "\u2696\ufe0f", "Aprobar / Rechazar Solicitud")
    ui.opcion(6, "\U0001f504", "Registrar Devolucion")
    ui.opcion(7, "\U0001f4ca", "Ver Reportes")
    ui.opcion(8, "\u270f\ufe0f", "Actualizar Vecino")
    ui.opcion(9, "\U0001f519", "Volver")


def menu_usuario():
    ui.seccion("\U0001f3e0  MENU VECINO")
    ui.opcion(1, "\U0001f50e", "Ver Herramientas Disponibles")
    ui.opcion(2, "\U0001f4e5", "Solicitar Prestamo")
    ui.opcion(3, "\U0001f4dc", "Ver Mi Historial")
    ui.opcion(4, "\U0001f519", "Volver")


def opciones_administrador():
    while True:
        menu_administrador()
        opcion = input("\n  Selecciona una opcion: ").strip()

        if opcion == "1":
            ui.subtitulo("Registrar nueva herramienta")
            nombre = input("  Nombre: ").strip()
            categoria = input("  Categoria: ").strip()
            cantidad = pedir_numero_entero("  Cantidad: ")
            valor = pedir_numero_entero("  Valor estimado: ")
            nueva = mod_herramientas.crear_herramienta(nombre, categoria, cantidad, valor)
            ui.exito("Herramienta registrada con ID " + str(nueva["id"]) + " - " + nueva["nombre"])

        elif opcion == "2":
            ui.subtitulo("Catalogo de herramientas")
            mostrar_tabla_herramientas()

        elif opcion == "3":
            ui.subtitulo("Registrar nuevo vecino")
            nombres = input("  Nombres: ").strip()
            apellidos = input("  Apellidos: ").strip()
            telefono = pedir_telefono("  Telefono (10 digitos): ")
            direccion = input("  Direccion: ").strip()
            nuevo = mod_usuarios.crear_usuario(nombres, apellidos, telefono, direccion, "residente")
            ui.exito("Vecino registrado con ID " + str(nuevo["id"]) + " - "
                     + nuevo["nombres"] + " " + nuevo["apellidos"])

        elif opcion == "4":
            ui.subtitulo("Directorio de vecinos")
            mostrar_tabla_vecinos()

        elif opcion == "5":
            ui.subtitulo("Solicitudes pendientes")
            pendientes = [p for p in mod_prestamos.listar_prestamos() if p["estado"] == "pendiente"]
            if not pendientes:
                ui.aviso("No hay solicitudes pendientes.")
            else:
                ui.linea()
                for p in pendientes:
                    print("  \u23f3 Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                          + " solicita " + str(p["cantidad"]) + " x " + nombre_herramienta(p["id_herramienta"]))
                ui.linea()
                id_prestamo = pedir_numero_entero("\n  Id del prestamo a procesar: ")
                decision = input("  Aprobar o Rechazar? (A/R): ").strip().upper()
                if decision == "A":
                    if mod_prestamos.aprobar_prestamo(id_prestamo):
                        ui.exito("Prestamo aprobado. Stock actualizado.")
                    else:
                        ui.error("No se pudo aprobar (sin stock suficiente o id invalido). Revisa el log.")
                elif decision == "R":
                    motivo = input("  Motivo del rechazo (opcional): ").strip()
                    if mod_prestamos.rechazar_prestamo(id_prestamo, motivo):
                        ui.exito("Prestamo rechazado.")
                    else:
                        ui.error("No se pudo rechazar. Verifica el id.")
                else:
                    ui.error("Opcion invalida. No se realizo ningun cambio.")

        elif opcion == "6":
            ui.subtitulo("Registrar devolucion")
            activos = [p for p in mod_prestamos.listar_prestamos() if p["estado"] == "activo"]
            if not activos:
                ui.aviso("No hay prestamos activos.")
            else:
                ui.linea()
                for p in activos:
                    print("  \U0001f4e4 Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                          + " tiene " + str(p["cantidad"]) + " x " + nombre_herramienta(p["id_herramienta"]))
                ui.linea()
                id_prestamo = pedir_numero_entero("\n  Id del prestamo devuelto: ")
                if mod_prestamos.devolver_prestamo(id_prestamo):
                    ui.exito("Devolucion registrada. Stock restaurado.")
                else:
                    ui.error("No se pudo registrar la devolucion. Verifica el id.")

        elif opcion == "7":
            ui.subtitulo("\U0001f4c9 Herramientas con stock bajo")
            bajos = mod_reportes.stock_bajo()
            if not bajos:
                ui.info("Ninguna herramienta esta por debajo del minimo.")
            for h in bajos:
                ui.item("\u26a0\ufe0f  " + h["nombre"] + " - " + str(h["cantidad_disponible"]) + " unidad(es)")

            ui.subtitulo("\U0001f4e4 Prestamos activos")
            activos = mod_reportes.prestamos_activos()
            if not activos:
                ui.info("No hay prestamos activos.")
            for p in activos:
                ui.item("Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                        + " - " + nombre_herramienta(p["id_herramienta"])
                        + " - vence el " + p["fecha_devolucion_estimada"])

            ui.subtitulo("\u23f0 Prestamos vencidos")
            vencidos = mod_reportes.prestamos_vencidos()
            if not vencidos:
                ui.info("No hay prestamos vencidos.")
            for p in vencidos:
                ui.item("\U0001f6a8 Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                        + " - " + nombre_herramienta(p["id_herramienta"])
                        + " - vencio el " + p["fecha_devolucion_estimada"])

            ui.subtitulo("\U0001f3c6 Herramientas mas solicitadas")
            top_h = mod_reportes.herramientas_mas_solicitadas()
            if not top_h:
                ui.info("Aun no hay solicitudes registradas.")
            for item in top_h:
                ui.item(item["nombre"] + " - " + str(item["veces"]) + " vez(ces)")

            ui.subtitulo("\U0001f465 Vecinos que mas solicitan")
            top_u = mod_reportes.usuarios_mas_solicitantes()
            if not top_u:
                ui.info("Aun no hay solicitudes registradas.")
            for item in top_u:
                ui.item(item["nombre"] + " - " + str(item["veces"]) + " vez(ces)")

        elif opcion == "8":
            ui.subtitulo("Actualizar datos de un vecino")
            mostrar_tabla_vecinos()
            id_usuario = pedir_numero_entero("\n  Id del vecino a actualizar: ")
            if mod_usuarios.buscar_usuario(id_usuario) is None:
                ui.error("Ese vecino no existe. Revisa el id en la lista de arriba.")
            else:
                print("\n  Que dato deseas actualizar?")
                ui.opcion(1, "\U0001f4de", "Telefono")
                ui.opcion(2, "\U0001f3e0", "Direccion")
                campo_opcion = input("\n  Opcion: ").strip()
                if campo_opcion == "1":
                    nuevo_valor = pedir_telefono("  Nuevo telefono (10 digitos): ")
                    if mod_usuarios.actualizar_usuario(id_usuario, "telefono", nuevo_valor):
                        ui.exito("Telefono actualizado correctamente.")
                    else:
                        ui.error("No se pudo actualizar.")
                elif campo_opcion == "2":
                    nuevo_valor = input("  Nueva direccion: ").strip()
                    if mod_usuarios.actualizar_usuario(id_usuario, "direccion", nuevo_valor):
                        ui.exito("Direccion actualizada correctamente.")
                    else:
                        ui.error("No se pudo actualizar.")
                else:
                    ui.error("Opcion invalida.")

        elif opcion == "9":
            break
        else:
            ui.error("Opcion invalida. Intenta de nuevo.")


def opciones_usuario():
    ui.subtitulo("Identificate")
    mostrar_tabla_vecinos()
    id_usuario = pedir_numero_entero("\n  Ingresa tu id de vecino: ")
    if mod_usuarios.buscar_usuario(id_usuario) is None:
        ui.error("Ese vecino no existe. Pide al administrador que te registre.")
        return
    ui.exito("Hola, " + nombre_usuario(id_usuario) + " \U0001f44b")

    while True:
        menu_usuario()
        opcion = input("\n  Selecciona una opcion: ").strip()

        if opcion == "1":
            ui.subtitulo("Herramientas disponibles")
            mostrar_tabla_herramientas(solo_disponibles=True)

        elif opcion == "2":
            ui.subtitulo("Solicitar un prestamo")
            mostrar_tabla_herramientas(solo_disponibles=True)
            id_herramienta = pedir_numero_entero("\n  Id de la herramienta: ")

            herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
            if herramienta is None:
                ui.error("Esa herramienta no existe. Revisa el id en la lista de arriba.")
            else:
                cantidad = pedir_numero_entero("  Cantidad: ")
                observaciones = input("  Observaciones: ").strip()

                if cantidad > herramienta["cantidad_disponible"]:
                    ui.aviso("Pediste " + str(cantidad) + " unidades, pero ahora mismo solo hay "
                             + str(herramienta["cantidad_disponible"]) + " disponibles.")
                    ui.aviso("La solicitud se enviara igual, pero es probable que sea rechazada.")

                solicitud = mod_prestamos.solicitar_prestamo(
                    id_usuario, id_herramienta, cantidad, observaciones)
                if solicitud:
                    ui.exito("Solicitud creada con ID " + str(solicitud["id"]) + " - "
                             + nombre_usuario(id_usuario) + " solicita " + str(cantidad)
                             + " x " + nombre_herramienta(id_herramienta))
                    ui.info("Espera la aprobacion del administrador.")
                else:
                    ui.error("No se pudo crear la solicitud.")

        elif opcion == "3":
            ui.subtitulo("Mi historial de prestamos")
            mios = [p for p in mod_prestamos.listar_prestamos() if p["id_usuario"] == id_usuario]
            if not mios:
                ui.aviso("Todavia no tienes prestamos registrados.")
            else:
                ui.linea()
                for p in mios:
                    print("  " + emoji_estado(p["estado"]) + " Prestamo " + str(p["id"]) + " - "
                          + nombre_herramienta(p["id_herramienta"]) + " - "
                          + str(p["cantidad"]) + " unidad(es) - " + p["estado"])
                ui.linea()

        elif opcion == "4":
            break
        else:
            ui.error("Opcion invalida. Intenta de nuevo.")


def main():
    ui.titulo("\U0001f527 SISTEMA DE PRESTAMO DE HERRAMIENTAS \U0001f528")
    ui.info("Junta comunal - prestamos entre vecinos")

    while True:
        ui.seccion("MENU PRINCIPAL")
        ui.opcion(1, "\U0001f9d1\u200d\U0001f4bc", "Entrar como Administrador")
        ui.opcion(2, "\U0001f3e0", "Entrar como Vecino")
        ui.opcion(3, "\U0001f6aa", "Salir")
        rol = input("\n  Selecciona una opcion: ").strip()

        if rol == "1":
            opciones_administrador()
        elif rol == "2":
            opciones_usuario()
        elif rol == "3":
            ui.despedida("\U0001f44b Hasta luego!")
            break
        else:
            ui.error("Opcion invalida. Intenta de nuevo.")


if __name__ == "__main__":
    main()