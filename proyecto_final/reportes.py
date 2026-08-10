from datetime import datetime
import herramientas as mod_herramientas
import usuarios as mod_usuarios
import prestamos as mod_prestamos

FORMATO_FECHA = "%Y-%m-%d"
STOCK_MINIMO = 3

def stock_bajo():
    return [h for h in mod_herramientas.listar_herramientas() if h["cantidad_disponible"] < STOCK_MINIMO]

def prestamos_activos():
    return [p for p in mod_prestamos.listar_prestamos() if p["estado"] == "activo"]

def prestamos_vencidos():
    hoy = datetime.now