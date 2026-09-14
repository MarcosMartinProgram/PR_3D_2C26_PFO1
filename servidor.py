import socket
import sqlite3
import threading
from datetime import datetime

# Constantes de red y persistencia
HOST = 'localhost'
PORT = 5000
DB_NAME = 'chat.db'


def inicializar_db():
    """Crea la tabla en SQLite si no existe."""
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        print(f"[ERROR BD] Fallo al inicializar la base de datos: {e}")
        raise


def guardar_mensaje(contenido, ip_cliente):
    """
    Inserta un mensaje en la BD.
    Se define timeout de 10s para prevenir bloqueos por accesos concurrentes de hilos.
    """
    try:
        # Timeout para evitar 'database is locked' en concurrencia
        conexion = sqlite3.connect(DB_NAME, timeout=10.0)
        cursor = conexion.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, timestamp, ip_cliente))

        conexion.commit()
        conexion.close()
        return timestamp
    except sqlite3.Error as e:
        print(f"[ERROR BD] Fallo al registrar el mensaje: {e}")
        return None


def inicializar_socket():
    """Configura el socket TCP/IP, habilita reutilización de puerto y comienza a escuchar."""
    try:
        # Configuración del socket TCP/IP (AF_INET = IPv4, SOCK_STREAM = TCP)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Permite reutilizar la dirección local inmediatamente si el proceso se reinicia
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}")
        return server_socket
    except OSError as e:
        print(f"[ERROR RED] No se pudo inicializar el socket (puerto posiblemente ocupado): {e}")
        return None


def atender_cliente(conn, addr):
    """Función de trabajo ejecutada dentro de un hilo independiente para cada cliente."""
    ip_cliente = addr[0]
    puerto_cliente = addr[1]
    hilo_actual = threading.current_thread().name
    print(f"[CONEXIÓN] Cliente conectado desde {ip_cliente}:{puerto_cliente} | Asignado a: {hilo_actual}")

    with conn:
        while True:
            try:
                datos = conn.recv(1024)
                if not datos:
                    # Desconexión abrupta del cliente
                    break

                mensaje = datos.decode('utf-8').strip()

                # Condición de salida solicitada
                if mensaje.lower() in ['éxito', 'exito']:
                    print(f"[CLIENTE] {ip_cliente}:{puerto_cliente} finalizó su sesión.")
                    break

                print(f"[{ip_cliente}:{puerto_cliente}] dice: {mensaje}")

                # Persistencia en base de datos
                timestamp = guardar_mensaje(mensaje, ip_cliente)

                if timestamp:
                    respuesta = f"Mensaje recibido: {timestamp}"
                else:
                    respuesta = "Error al guardar el mensaje en la base de datos."

                # Respuesta al cliente
                conn.sendall(respuesta.encode('utf-8'))

            except ConnectionResetError:
                print(f"[AVISO] Conexión reseteada inesperadamente por {ip_cliente}:{puerto_cliente}")
                break

    print(f"[CONEXIÓN CERRADA] Sesión finalizada con {ip_cliente}:{puerto_cliente}")


def iniciar_servidor():
    """Bucle principal del servidor que despacha cada conexión entrante a un nuevo hilo."""
    try:
        inicializar_db()
    except Exception:
        print("[CRÍTICO] Abortando servidor por fallo en base de datos.")
        return

    server_socket = inicializar_socket()
    if not server_socket:
        return

    try:
        while True:
            # accept() bloquea hasta recibir una conexión entrante
            conn, addr = server_socket.accept()

            # Creación y lanzamiento de un hilo exclusivo para el cliente
            # daemon=True garantiza que los hilos no bloqueen el cierre del servidor al presionar Ctrl+C
            hilo_cliente = threading.Thread(
                target=atender_cliente,
                args=(conn, addr),
                daemon=True
            )
            hilo_cliente.start()

            # Clientes concurrentes activos (hilos totales menos el principal)
            print(f"[HILOS] Clientes activos simultáneamente: {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n[SERVIDOR] Deteniendo servidor por interrupción del usuario...")
    finally:
        server_socket.close()


if __name__ == '__main__':
    iniciar_servidor()