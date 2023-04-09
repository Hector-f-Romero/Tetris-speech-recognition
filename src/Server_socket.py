import socket

class ServerSocket():
    def __init__(self, name,port):
        self._port = port
        self._socket = socket.socket()
        self.config_socket()

    def config_socket(self):
        self._socket.bind(("localhost",self._port))
        self._socket.listen(5)

    # def notify(self,change):
    #     print(f"Se actualizó el valor a: {change.data} - {change.name}")

    def start_socket_server(self):
        print("Servidor configurado 👻")
        try:
            while True:
                clientConnected,addr = self._socket.accept()
                print(f"Conexión establecida con {addr}")
                respuesta = clientConnected.recv(1024)
                print(respuesta.decode())
                # self.notify()
                # func(selfPy)
                
                clientConnected.close()
        except KeyboardInterrupt:
            print('interrupted!')
