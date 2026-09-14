import sqlite3

def mostrar_mensajes():
    try:
        conexion = sqlite3.connect('chat.db')
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id, contenido, fecha_envio, ip_cliente FROM mensajes")
        filas = cursor.fetchall()
        
        if not filas:
            print("[INFO] La base de datos está vacía.")
            return

        print("-" * 75)
        print(f"{'ID':<4} | {'FECHA':<20} | {'IP CLIENTE':<15} | {'MENSAJE'}")
        print("-" * 75)
        for fila in filas:
            id_msg, contenido, fecha, ip = fila
            print(f"{id_msg:<4} | {fecha:<20} | {ip:<15} | {contenido}")
        print("-" * 75)
        
        conexion.close()
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo leer la base de datos: {e}")

if __name__ == '__main__':
    mostrar_mensajes()