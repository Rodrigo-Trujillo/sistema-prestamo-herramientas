from persistencia import cargar, guardar, siguiente_id
from logs import registrar_evento

ARCHIVO = "usuarios.json"


def crear_usuario(nombres, apellidos, telefono, direccion, tipo):
    usuarios = cargar(ARCHIVO)
    nuevo = {
        "id": siguiente_id(usuarios),
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "direccion": direccion,
        "tipo_usuario": tipo
    }
    usuarios.append(nuevo)
    guardar(ARCHIVO, usuarios)
    registrar_evento("Usuario creado: " + nombres + " " + apellidos)
    return nuevo


def listar_usuarios():
    return cargar(ARCHIVO)


def buscar_usuario(id_usuario):
    for usuario in cargar(ARCHIVO):
        if usuario["id"] == id_usuario:
            return usuario
    return None


def actualizar_usuario(id_usuario, campo, nuevo_valor):
    usuarios = cargar(ARCHIVO)
    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            usuario[campo] = nuevo_valor
            guardar(ARCHIVO, usuarios)
            return True
    return False


def eliminar_usuario(id_usuario):
    usuarios = cargar(ARCHIVO)
    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            usuarios.remove(usuario)
            guardar(ARCHIVO, usuarios)
            return True
    return False