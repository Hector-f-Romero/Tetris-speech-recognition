# # Definir la variable compartida
# shared_variable = None

# # Función para obtener el valor de la variable compartida
# def get_shared_variable():
#     return shared_variable

# # Función para actualizar el valor de la variable compartida
# def set_shared_variable(value):
#     global shared_variable
#     shared_variable = value

import multiprocessing

class AccionTomada:
    def __init__(self):
        # self.valor = multiprocessing.Value('i', 6)  # Creamos un valor compartido de tipo entero
        # self.cola = multiprocessing.Queue()  # Creamos una cola compartida
        self.accion_tomada = 6
    
    # def actualizar_valor(self, nuevo_valor):
    #     with self.valor.get_lock():
    #         self.valor.value = nuevo_valor  # Actualizamos el valor compartido
    #     self.cola.put(nuevo_valor)  # Enviamos el nuevo valor a la cola
    
    # def obtener_valor(self):
    #     return self.valor.value  # Obtenemos el valor actual de la variable compartida
    #     # return self.cola.get()
    def getAccion_tomada(self):
        return self.accion_tomada
    
    def setAccion_tomada(self, accion_tomada):
        self.accion_tomada = accion_tomada
