import socket

HOST = 'localhost'
PORT = 5000


def iniciar_cliente():
    """Conecta al servidor, permite enviar mensajes interactivos y muestra respuestas."""
    try:
        # Configuración del socket TCP/IP del cliente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conexión al socket del servidor
        client_socket.connect((HOST, PORT))
        print(f"[CONECTADO] Conexión exitosa a {HOST}:{PORT}")
        print("Escribí tus mensajes. Ingresá 'éxito' para finalizar la conexión.\n")

        with client_socket:
            while True:
                mensaje = input("Vos > ")

                if not mensaje.strip():
                    continue

                # Envío del mensaje codificado en bytes
                client_socket.sendall(mensaje.encode('utf-8'))

                # Salir si el comando es éxito (con o sin tilde)
                if mensaje.strip().lower() in ['éxito', 'exito']:
                    print("[DESCONECTANDO] Cerrando sesión...")
                    break

                # Espera de la confirmación del servidor
                respuesta = client_socket.recv(1024).decode('utf-8')
                print(f"Servidor > {respuesta}\n")

    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar al servidor. Verificá que esté corriendo.")
    except Exception as e:
        print(f"[ERROR] Ocurrió un fallo en la comunicación: {e}")


if __name__ == '__main__':
    iniciar_cliente()