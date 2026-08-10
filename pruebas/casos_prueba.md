# Casos de prueba — Sistema de Préstamo de Herramientas Comunitarias

Instrucciones: ejecuten el programa (`python main.py`) siguiendo cada caso en
orden, y llenen las columnas **RESULTADO OBTENIDO** y **ESTADO** con lo que
realmente pasó. Si algo no coincide con lo esperado, el ESTADO es `ERROR` —
se documenta igual, no se oculta.

| CASO N° | ENTRADAS | OPERACIÓN | RESULTADO ESPERADO | RESULTADO OBTENIDO | ESTADO |
|---|---|---|---|---|---|
| 1 | nombre="Taladro", categoria="Construccion", cantidad=5, valor=600000 | `crear_herramienta(...)` | Se crea con id 1, estado "activa" | Se creó correctamente: `1 - Taladro - 5 disp. - activa` | OK |
| 2 | nombres="Ana", apellidos="Gomez", telefono, direccion | `crear_usuario(...)` | Se crea con id 1, tipo "residente" | "Vecino Registrado." Se corrigió un bug en usuarios.py (faltaban imports, typo en siguiente_id, e indentación incorrecta en buscar/actualizar/eliminar) | OK (tras corrección) |
| 3 | id_usuario=1, id_herramienta=1, cantidad=2 | `solicitar_prestamo(...)` | Préstamo creado con estado "pendiente" | "Solicitud creada con id 1 - espera aprobacion." | OK |
| 4 | id_prestamo=1 (herramienta con 5 disponibles) | `aprobar_prestamo(1)` | Devuelve True; stock de la herramienta baja de 5 a 3 | "Prestamo Aprobado." Stock confirmado en 3 | OK |
| 5 | id_usuario=1, id_herramienta=1, cantidad=50 (solo quedan 3) | `solicitar_prestamo(...)` seguido de `aprobar_prestamo(...)` | Devuelve False; el préstamo queda en estado "rechazado"; el stock NO cambia | "No se pudo aprobar. Revisa el log." Stock se mantuvo en 3 | OK |
| 6 | (después del caso 5) | Revisar `logs/eventos.log` | Debe aparecer una línea registrando el rechazo por falta de stock | Línea confirmada: "RECHAZADO prestamo 2: se pidieron 50 y solo hay 3" | OK |
| 7 | id_prestamo=1 | `devolver_prestamo(1)` | Devuelve True; el estado pasa a "devuelto"; el stock vuelve de 3 a 5 | "Devolucion registrada." Stock confirmado en 5 | OK |
| 8 | (sin datos, tras los casos anteriores) | `stock_bajo()` | Lista las herramientas con menos de 3 unidades disponibles | Lista vacía (correcto, el Taladro tiene 5 unidades) | OK |
| 9 | (sin datos) | `prestamos_activos()` | Lista los préstamos en estado "activo" | Lista vacía (correcto, el único préstamo activo ya fue devuelto) | OK |
| 10 | (sin datos) | `herramientas_mas_solicitadas()` | Lista ordenada de mayor a menor por número de solicitudes | "Taladro - 2 vez(ces)". Se conectó la función al menú (opción 7 de main.py solo mostraba 2 de los 5 reportes) | OK (tras conexión) |
| 11 | (sin datos) | `usuarios_mas_solicitantes()` | Lista ordenada de mayor a menor por número de solicitudes | "Ana Gomez - 2 vez(ces)" | OK |
| 12 | (opción de menú inexistente, ej. "9") | Menú de administrador | El programa muestra "Opción inválida" y no se cierra | "Opcion invalida." Programa continuó funcionando | OK |
| 13 | texto en vez de número (ej. "abc" en cantidad) | `pedir_numero_entero(...)` | El programa pide de nuevo sin cerrarse | "Debes ingresar un numero entero" y volvió a pedir el dato | OK |

## Notas

- El caso 5 fue el más importante de todos: confirma que el sistema **no
  permite** prestar más unidades de las disponibles, y que ese intento
  queda registrado como evento en el log.
- Durante las pruebas se encontraron y corrigieron 2 bugs reales:
  1. `usuarios.py` no importaba `persistencia` ni `logs`, tenía un typo
     (`sigiente_id`), y las funciones `buscar_usuario`, `actualizar_usuario`
     y `eliminar_usuario` tenían errores de indentación que hacían que
     fallaran con cualquier elemento que no fuera el primero de la lista.
  2. `main.py` solo conectaba 2 de los 5 reportes de `reportes.py` al menú
     de "Ver Reportes" — se completó para mostrar los 5.
- Todas las pruebas se ejecutaron directamente en la terminal del proyecto,
  con `python main.py`, en la máquina de Rodrigo Trujillo.
