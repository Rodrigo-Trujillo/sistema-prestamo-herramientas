# Sistema de Préstamo de Herramientas Comunitarias

Programa de consola en Python para gestionar el préstamo de herramientas
entre vecinos de un barrio. Reemplaza el control manual (cuadernos, llamadas)
por un sistema digital organizado, con roles diferenciados, validaciones,
registro de eventos y una interfaz con colores y emojis.

## Equipo de desarrollo
- Rodrigo Trujillo
- Dainer Pereira
- Sebastián Panche

## Requisitos
- Python 3.8 o superior
- Terminal con soporte de colores ANSI (Windows Terminal, VS Code, la mayoría
  de terminales modernas)

## Cómo ejecutarlo
1. Descargar o clonar este repositorio
2. Abrir una terminal dentro de la carpeta del proyecto
3. Ejecutar:
```
python main.py
```

## Estructura del proyecto
```
sistema-prestamo-herramientas/
├── main.py            → menú principal, roles y toda la interacción con el usuario
├── estilos.py          → colores, emojis y tablas para la interfaz de consola
├── herramientas.py    → CRUD de herramientas (crear, listar, buscar, actualizar, inactivar)
├── usuarios.py        → CRUD de vecinos (crear, listar, buscar, actualizar, eliminar)
├── prestamos.py       → solicitudes, aprobación, rechazo y devolución
├── reportes.py        → consultas y reportes
├── persistencia.py    → lectura y escritura de archivos JSON
├── logs.py            → registro de eventos
├── datos/             → archivos JSON generados automáticamente (no se sube a git)
├── logs/              → archivo de eventos generado automáticamente (no se sube a git)
├── pruebas/           → casos de prueba documentados
└── README.md          → este archivo
```

## Roles y operaciones disponibles

**Administrador** — menú de 14 opciones agrupadas en 3 bloques:

*Herramientas*
- Registrar, Listar, Buscar, Actualizar (nombre/categoría/valor), Inactivar

*Vecinos*
- Registrar, Listar, Buscar, Actualizar (teléfono/dirección), Eliminar

*Préstamos y reportes*
- Aprobar o Rechazar solicitudes (con motivo opcional)
- Registrar Devolución
- Ver Reportes (stock bajo, préstamos activos, préstamos vencidos,
  herramientas más solicitadas, vecinos que más solicitan)

**Vecino** — menú de 4 opciones:
- Ver herramientas disponibles
- Solicitar un préstamo
- Ver su historial de préstamos

## Flujo de un préstamo
1. El vecino crea una solicitud → estado: **pendiente**. Si pide más
   unidades de las disponibles en ese momento, el sistema le avisa antes de
   enviarla.
2. El administrador revisa las solicitudes pendientes y decide: **aprobar**
   o **rechazar** (con un motivo opcional que queda registrado en el log).
3. Al aprobar, el sistema vuelve a verificar el stock disponible en ese
   instante. Si no alcanza, la solicitud se rechaza automáticamente y queda
   registrado el evento.
4. Si se aprueba → estado: **activo** y se descuenta el stock.
5. Cuando se devuelve → estado: **devuelto** y se restaura el stock.

## Validaciones implementadas
- El teléfono de un vecino debe tener exactamente 10 dígitos numéricos.
- Los campos de texto obligatorios (nombre, apellidos, dirección, categoría)
  no pueden quedar vacíos.
- La cantidad y el valor estimado de una herramienta deben ser mayores a
  cero.
- No se puede solicitar una herramienta que no existe o que está marcada
  como "fuera de servicio".
- Cualquier entrada de menú fuera de las opciones válidas muestra un aviso
  y no cierra el programa.
- Todas las opciones numéricas (`input`) están protegidas contra texto no
  numérico.

## Archivos generados por el programa
- `datos/herramientas.json` → herramientas registradas
- `datos/usuarios.json` → vecinos registrados
- `datos/prestamos.json` → préstamos registrados
- `logs/eventos.log` → historial de eventos (creaciones, aprobaciones,
  rechazos con motivo, devoluciones)

## Pruebas
La carpeta `pruebas/casos_prueba.md` documenta los casos de prueba
ejecutados, incluyendo los intentos deliberados de romper el programa
(cantidades negativas, campos vacíos, herramientas inactivas, archivos JSON
dañados) y las correcciones aplicadas a partir de esas pruebas.
