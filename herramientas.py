from persistencia import cargar, guardar, siguiente_id
from logs import registrar_evento

ARCHIVO = "herramientas.json"


def crear_herramienta(nombre, categoria, cantidad, valor):
    herramientas = cargar(ARCHIVO)
    nueva = {
        "id": siguiente_id(herramientas),
        "nombre": nombre,
        "categoria": categoria,
        "cantidad_disponible": cantidad,
        "estado": "activa",
        "valor_estimado": valor
    }
    herramientas.append(nueva)
    guardar(ARCHIVO, herramientas)
    registrar_evento("Herramienta creada: " + nombre + " (id " + str(nueva["id"]) + ")")
    return nueva


def listar_herramientas():
    return cargar(ARCHIVO)


def buscar_herramienta(id_herramienta):
    for herramienta in cargar(ARCHIVO):
        if herramienta["id"] == id_herramienta:
            return herramienta
    return None


def actualizar_herramienta(id_herramienta, campo, nuevo_valor):
    herramientas = cargar(ARCHIVO)
    for herramienta in herramientas:
        if herramienta["id"] == id_herramienta:
            herramienta[campo] = nuevo_valor
            guardar(ARCHIVO, herramientas)
            registrar_evento("Herramienta " + str(id_herramienta) + ": " + campo + " cambiado")
            return True
    return False


def inactivar_herramienta(id_herramienta):
    return actualizar_herramienta(id_herramienta, "estado", "fuera de servicio")