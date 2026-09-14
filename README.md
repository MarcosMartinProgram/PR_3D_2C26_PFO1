# Propuesta Formativa Obligatoria: Chat Cliente-Servidor TCP con Sockets y SQLite (Multihilo)

**Asignatura:** Programación sobre Redes  
**Carrera:** Tecnicatura Universitaria en Desarrollo de Software  

---

## 📋 Descripción del Proyecto

Este proyecto consiste en la implementación de una arquitectura cliente-servidor basada en sockets TCP/IP utilizando Python puro (biblioteca estándar). El servidor escucha peticiones entrantes de manera concurrente gracias a un esquema de concurrencia basado en hilos (`threading`), almacena cada mensaje recibido en una base de datos local **SQLite** con su respectiva metadata (dirección IP, timestamp y contenido) y responde al cliente con una confirmación que incluye la marca de tiempo de recepción.

---

## 🚀 Características Principales

- **Concurrencia con Hilos (`threading`):** Manejo simultáneo de múltiples clientes sin bloquear el bucle de escucha principal (`accept`).
- **Persistencia en SQLite (`sqlite3`):** Registro transaccional seguro contra condiciones de carrera mediante timeouts de bloqueo.
- **Protocolo de Comunicación Robusto:**
  - Configuración de socket con opción `SO_REUSEADDR` para rápida recuperación tras reinicios.
  - Decodificación segura en `utf-8`.
  - Finalización de sesión controlada mediante la palabra clave `éxito` (o `exito`).
- **Manejo de Errores y Excepciones:** Detección de puertos ocupados (`OSError`), conexiones reseteadas inesperadamente por clientes (`ConnectionResetError`) y errores de acceso o escritura a nivel base de datos (`sqlite3.Error`).

---

## 📂 Estructura del Repositorio

```text
├── .gitignore         # Archivos ignorados por Git (.venv, __pycache__, chat.db, etc.)
├── README.md          # Documentación general del práctico
├── servidor.py        # Servidor TCP multihilo y controlador de base de datos
├── cliente.py         # Cliente interactivo por consola
└── ver_db.py          # Script utilitario para consultar y tabular la base de datos
```

---

## ⚙️ Requisitos Previos

- **Python 3.8 o superior** instalado en el sistema.
- No se requieren librerías de terceros (`pip`), ya que la solución utiliza exclusivamente la biblioteca estándar:
  - `socket`
  - `threading`
  - `sqlite3`
  - `datetime`

---

## 🛠️ Guía de Ejecución y Pruebas

Se recomienda abrir dos o más terminales para probar la concurrencia en local.

### 1. Iniciar el Servidor

En la primera terminal, ejecutá el servidor:

```bash
python servidor.py
```

Salida esperada:
```text
[SERVIDOR] Escuchando en localhost:5000
```

### 2. Iniciar el Cliente

En una segunda terminal (y opcionalmente en una tercera para probar multihilo), iniciá el cliente:

```bash
python cliente.py
```

Interacción en la terminal del cliente:
```text
[CONECTADO] Conexión exitosa a localhost:5000
Escribí tus mensajes. Ingresá 'éxito' para finalizar la conexión.

Vos > Hola servidor
Servidor > Mensaje recibido: 2026-09-14 18:05:12

Vos > éxito
[DESCONECTANDO] Cerrando sesión...
```

---

## 🗄️ Inspección de la Base de Datos

Cada mensaje enviado se almacena automáticamente en el archivo `chat.db` dentro de la tabla `mensajes`:

| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Identificador único del registro |
| `contenido` | `TEXT` | Texto enviado por el cliente |
| `fecha_envio` | `TEXT` | Timestamp de recepción (`YYYY-MM-DD HH:MM:SS`) |
| `ip_cliente` | `TEXT` | Dirección IP de origen de la conexión |

Para verificar los registros almacenados podés usar el script auxiliar `ver_db.py`:

```bash
python ver_db.py
```

Ejemplo de salida:
```text
---------------------------------------------------------------------------
ID   | FECHA                | IP CLIENTE      | MENSAJE
---------------------------------------------------------------------------
1    | 2026-09-14 18:05:12  | 127.0.0.1       | Hola servidor
---------------------------------------------------------------------------
```