import socket

mi_socket = socket.socket()
mi_socket.connect(("localhost",8001))
# mi_socket.send("Hola desde el cliente")
# recibe 1024 bits

# conexion,addr = mi_socket.accept()
# print(f"Conexión establecida con {addr}")
mensaje = "Hola desde el cliente."
mi_socket.send(mensaje.encode())
mi_socket.close()