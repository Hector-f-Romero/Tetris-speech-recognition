import socket

# Genera el socket del servidor con los valores por defecto
mi_socket = socket.socket()

mi_socket.bind(("localhost",8001))
mi_socket.listen(5)

print("Servidor configurado 👻")

try:
    while True:
        clientConnected,addr = mi_socket.accept()
        print(f"Conexión establecida con {addr}")
        mensaje = "Hola desde el servidor."
        # conexion.send(mensaje.encode())
        respuesta = clientConnected.recv(1024)
        print(respuesta.decode())
        clientConnected.close()
except KeyboardInterrupt:
            print('interrupted!')
    