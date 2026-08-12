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
| 14 | id_herramienta=1 (Taladro) | `buscar_herramienta(1)` desde "Buscar Herramienta" | Muestra la ficha completa: id, nombre, categoria, disponible, estado, valor estimado | Mostró correctamente todos los campos del Taladro | OK |
| 15 | id_herramienta=1, campo="nombre", nuevo valor="Taladro Bosch" | `actualizar_herramienta(...)` desde "Actualizar Herramienta" | Devuelve True; el nombre queda actualizado | "Herramienta actualizada correctamente." Nombre confirmado como "Taladro Bosch" en el listado | OK |
| 16 | id_herramienta=2 (Pala) | `inactivar_herramienta(2)` desde "Inactivar Herramienta" | Devuelve True; el estado pasa a "fuera de servicio" | "Herramienta marcada como 'fuera de servicio'." Confirmado en el listado | OK |
| 17 | id_usuario=1 (Ana Gomez) | `buscar_usuario(1)` desde "Buscar Vecino" | Muestra la ficha completa: id, nombre, telefono, direccion, tipo de usuario | Mostró correctamente todos los datos de Ana Gomez | OK |
| 18 | id_usuario=2 (Dainer Cuteño), confirmar con "S" | `eliminar_usuario(2)` desde "Eliminar Vecino" | El vecino se elimina de la lista; los ids de los demás vecinos NO se recorren (no se renumeran) | "Vecino eliminado correctamente." Listado final quedó con ids 1, 3, 4 (sin el 2) — confirmado que no se reordenan | OK |
| 19 | Nombres, Apellidos y Direccion dejados en blanco (Enter sin escribir nada) al registrar un vecino | Registrar Vecino desde el menu | El programa no debe permitir avanzar con campos obligatorios vacios | Antes del ajuste: SI dejaba avanzar y creaba un vecino "fantasma" sin nombre. Se agrego `pedir_texto_obligatorio()` y ahora rechaza el vacio con "Este campo no puede quedar vacio." hasta llenarlo | OK (tras corrección) |
| 20 | cantidad=0 y cantidad=-5 al registrar una herramienta | Registrar Herramienta desde el menu | No debe permitir registrar una herramienta con stock cero o negativo | Antes del ajuste: SI permitia registrar un "Serrucho" con -5 unidades. Se agrego `pedir_numero_positivo()` y ahora responde "El numero debe ser mayor que cero." | OK (tras corrección) |
| 21 | cantidad=-3 al solicitar un prestamo, luego aprobarlo | Solicitar Prestamo + Aprobar | No debe permitir cantidades negativas | Antes del ajuste: al aprobar un prestamo de -3 unidades, el stock AUMENTABA de 5 a 8 (se "creaban" herramientas de la nada). Corregido con `pedir_numero_positivo()` | OK (tras corrección) |
| 22 | id de una herramienta marcada como "fuera de servicio", escrito directamente | Solicitar Prestamo desde el menu vecino | No debe permitir solicitar una herramienta inactiva | Antes del ajuste: la herramienta no aparecia en la lista, pero al escribir su id directamente SI se podia solicitar y aprobar. Ahora responde "Esa herramienta no esta disponible (estado: fuera de servicio)." | OK (tras corrección) |
| 23 | Archivo `datos/herramientas.json` modificado a mano con contenido invalido | `cargar()` en persistencia.py | El programa no debe romperse; debe avisar y continuar con lista vacia | "El archivo está dañado. Se inicia con lista vacía." El programa continuo funcionando sin cerrarse | OK (sin necesidad de corrección) |

## Notas

- El caso 5 fue el más importante de todos: confirma que el sistema **no
  permite** prestar más unidades de las disponibles, y que ese intento
  queda registrado como evento en el log.
- El caso 18 confirma un comportamiento de diseño intencional, no un error:
  los ids son una etiqueta permanente de cada registro, no una posición que
  se reacomoda al eliminar. Los préstamos guardan `id_usuario` como
  referencia — si el sistema recorriera los ids al eliminar a alguien,
  cualquier préstamo histórico apuntaría a la persona equivocada. Por eso
  `siguiente_id()` nunca "rellena huecos": solo calcula el id más alto
  existente + 1.
- Durante las pruebas se encontraron y corrigieron 2 bugs reales:
  1. `usuarios.py` no importaba `persistencia` ni `logs`, tenía un typo
     (`sigiente_id`), y las funciones `buscar_usuario`, `actualizar_usuario`
     y `eliminar_usuario` tenían errores de indentación que hacían que
     fallaran con cualquier elemento que no fuera el primero de la lista.
  2. `main.py` solo conectaba 2 de los 5 reportes de `reportes.py` al menú
     de "Ver Reportes" — se completó para mostrar los 5.
- Los casos 14-18 se agregaron al completar las operaciones CRUD que faltaban
  según la rúbrica del proyecto (Buscar y Actualizar para Herramientas;
  Buscar y Eliminar para Vecinos), que ya existían como funciones en los
  módulos pero no estaban conectadas al menú de `main.py`.
- Los casos 19 a 22 son especialmente valiosos porque el programa **no se
  rompia** en ninguno de ellos: aceptaba silenciosamente datos invalidos
  (un vecino sin nombre, una herramienta con stock negativo, un prestamo
  que aumentaba el inventario en vez de reducirlo). Son fallas mas dificiles
  de detectar que un error visible, y se encontraron probando a proposito
  entradas que un usuario normal no escribiria.
- El caso 23 es el unico de este grupo que paso sin necesidad de corregir
  nada: el `try/except` de `persistencia.py` ya protegia contra archivos JSON
  danados desde el inicio.
- Todas las pruebas se ejecutaron directamente en la terminal del proyecto,
  con `python main.py`, en la máquina de Rodrigo Trujillo.
