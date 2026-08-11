from datetime import datetime, timedelta
from persistencia import cargar, guardar, siguiente_id
from logs import registrar_evento
import herramientas as mod_herramientas

ARCHIVO = "prestamos.json"
FORMATO_FECHA = "%Y-%m-%d"
DIAS_PRESTAMO = 7

def solicitar_prestamo(id_usuario, id_herramienta, cantidad, observaciones=""):
    herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
    if herramienta is None:
        registrar_evento("Solicitud fallida: herramienta no existe")
        return None
    prestamos = cargar(ARCHIVO)
    hoy = datetime.now()
    nuevo = {
        "id": siguiente_id(prestamos),
        "id_usuario": id_usuario,
        "id_herramienta": id_herramienta,
        "cantidad": cantidad,
        "fecha_inicio": hoy.strftime(FORMATO_FECHA),
        "fecha_devolucion_estimada": (hoy + timedelta(days=DIAS_PRESTAMO)).strftime(FORMATO_FECHA),
        "estado": "pendiente",
        "observaciones": observaciones
    }
    prestamos.append(nuevo)
    guardar(ARCHIVO, prestamos)
    registrar_evento("Solicitud creada: prestamo " + str(nuevo["id"]))
    return nuevo

def aprobar_prestamo(id_prestamo):
    prestamos = cargar(ARCHIVO)
    for prestamo in prestamos:
        if prestamo["id"] == id_prestamo:
            if prestamo["estado"] != "pendiente":
                return False
            herramienta = mod_herramientas.buscar_herramienta(prestamo["id_herramienta"])
            if herramienta is None:
                return False
            if herramienta["cantidad_disponible"] < prestamo["cantidad"]:
                prestamo["estado"] = "rechazado"
                guardar(ARCHIVO, prestamos)
                registrar_evento("RECHAZADO prestamo " + str(id_prestamo) + ": se pidieron " + str(prestamo["cantidad"]) + " y solo hay " + str(herramienta["cantidad_disponible"]))
                return False
            nueva_cantidad = herramienta["cantidad_disponible"] - prestamo["cantidad"]
            mod_herramientas.actualizar_herramienta(herramienta["id"], "cantidad_disponible", nueva_cantidad)
            prestamo["estado"] = "activo"
            guardar(ARCHIVO, prestamos)
            registrar_evento("Prestamo " + str(id_prestamo) + " aprobado")
            return True
    return False

def devolver_prestamo(id_prestamo):
    prestamos = cargar(ARCHIVO)
    for prestamo in prestamos:
        if prestamo["id"] == id_prestamo:
            if prestamo["estado"] != "activo":
                return False
            herramienta = mod_herramientas.buscar_herramienta(prestamo["id_herramienta"])
            if herramienta is not None:
                nueva_cantidad = herramienta["cantidad_disponible"] + prestamo["cantidad"]
                mod_herramientas.actualizar_herramienta(herramienta["id"], "cantidad_disponible", nueva_cantidad)
            prestamo["estado"] = "devuelto"
            guardar(ARCHIVO, prestamos)
            registrar_evento("Prestamo " + str(id_prestamo) + " devuelto")
            return True
    return False

def listar_prestamos():
    return cargar(ARCHIVO)


def rechazar_prestamo(id_prestamo, motivo=""):
    prestamos = cargar(ARCHIVO)
    for prestamo in prestamos:
        if prestamo["id"] == id_prestamo:
            if prestamo["estado"] != "pendiente":
                return False
            prestamo["estado"] = "rechazado"
            if motivo:
                prestamo["observaciones"] = prestamo.get("observaciones", "") + " | Rechazado por administrador: " + motivo
            guardar(ARCHIVO, prestamos)
            mensaje = "Prestamo " + str(id_prestamo) + " rechazado por el administrador"
            if motivo:
                mensaje += ": " + motivo
            registrar_evento(mensaje)
            return True
    return False