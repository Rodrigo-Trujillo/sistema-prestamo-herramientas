# Sistema de Préstamo de Herramientas Comunitarias

Programa de consola en Python para gestionar el préstamo de herramientas
entre vecinos de un barrio. Reemplaza el control manual (cuadernos, llamadas)
por un sistema digital organizado.

## Equipo de desarrollo
- Rodrigo Trujillo
- Dainer Pereira
- Sebastián Panche

## Requisitos
- Python 3.8 o superior

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
├── main.py            → menú principal y roles
├── herramientas.py    → catálogo de herramientas
├── usuarios.py        → directorio de vecinos
├── prestamos.py       → solicitudes, aprobación y devolución
├── reportes.py        → consultas y reportes
├── persistencia.py    → lectura y escritura de archivos JSON
├── logs.py            → registro de eventos
├── datos/             → archivos JSON generados automáticamente
├── logs/              → archivo de eventos generado automáticamente
├── pruebas/           → casos de prueba
└── README.md          → este archivo
```

## Roles

**Administrador:**
- Registra herramientas y vecinos
- Aprueba o rechaza solicitudes de préstamo
- Registra devoluciones
- Consulta reportes del sistema

**Vecino:**
- Consulta herramientas disponibles
- Crea solicitudes de préstamo
- Revisa su historial de préstamos

## Flujo de un préstamo
1. El vecino crea una solicitud → estado: **pendiente**
2. El administrador la aprueba o rechaza
3. Si se aprueba → estado: **activo** y se descuenta el stock
4. Cuando se devuelve → estado: **devuelto** y se restaura el stock

## Archivos generados por el programa
- `datos/herramientas.json` → herramientas registradas
- `datos/usuarios.json` → vecinos registrados
- `datos/prestamos.json` → préstamos registrados
- `logs/eventos.log` → historial de eventos
