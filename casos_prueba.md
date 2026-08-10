# Casos de prueba — Sistema de Préstamo de Herramientas Comunitarias

Instrucciones: ejecuten el programa (`python main.py`) siguiendo cada caso en
orden, y llenen las columnas **RESULTADO OBTENIDO** y **ESTADO** con lo que
realmente pasó. Si algo no coincide con lo esperado, el ESTADO es `ERROR` —
se documenta igual, no se oculta.

| CASO N° | ENTRADAS | OPERACIÓN | RESULTADO ESPERADO | RESULTADO OBTENIDO | ESTADO |
|---|---|---|---|---|---|
| 1 | nombre="Taladro", categoria="Construccion", cantidad=5, valor=600000 | `crear_herramienta(...)` | Se crea con id 1, estado "activa" | | |
| 2 | nombres="Ana", apellidos="Gomez", telefono, direccion | `crear_usuario(...)` | Se crea con id 1, tipo "residente" | | |
| 3 | id_usuario=1, id_herramienta=1, cantidad=2 | `solicitar_prestamo(...)` | Préstamo creado con estado "pendiente" | | |
| 4 | id_prestamo=1 (herramienta con 5 disponibles) | `aprobar_prestamo(1)` | Devuelve True; stock de la herramienta baja de 5 a 3 | | |
| 5 | id_usuario=1, id_herramienta=1, cantidad=50 (solo quedan 3) | `solicitar_prestamo(...)` seguido de `aprobar_prestamo(...)` | Devuelve False; el préstamo queda en estado "rechazado"; el stock NO cambia | | |
| 6 | (después del caso 5) | Revisar `logs/eventos.log` | Debe aparecer una línea registrando el rechazo por falta de stock | | |
| 7 | id_prestamo=1 | `devolver_prestamo(1)` | Devuelve True; el estado pasa a "devuelto"; el stock vuelve de 3 a 5 | | |
| 8 | (sin datos, tras los casos anteriores) | `stock_bajo()` | Lista las herramientas con menos de 3 unidades disponibles | | |
| 9 | (sin datos) | `prestamos_activos()` | Lista los préstamos en estado "activo" | | |
| 10 | id_usuario=1 | `historial_usuario(1)` | Lista todos los préstamos hechos por ese usuario | | |
| 11 | (sin datos) | `herramientas_mas_solicitadas()` | Lista ordenada de mayor a menor por número de solicitudes | | |
| 12 | (opción de menú inexistente, ej. "9") | Menú principal o menú de administrador | El programa muestra "Opción inválida" y no se cierra | | |
| 13 | texto en vez de número (ej. "abc" en cantidad) | `pedir_numero_entero(...)` | El programa pide de nuevo sin cerrarse | | |

## Notas

- El caso 5 es el más importante de todos: prueba que el sistema **no permite**
  prestar más unidades de las disponibles, y que ese intento queda registrado
  como evento.
- Si algún caso da ESTADO = ERROR, anoten debajo una breve explicación de qué
  pasó, para poder corregirlo antes de la entrega final.
