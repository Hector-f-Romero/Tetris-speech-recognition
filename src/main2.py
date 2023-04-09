import speech_recognition as sr
from settings import *
from tetris import Tetris,Text
import sys
import pathlib
import time
import joblib
import pygame as pg
import socket

from preprocesamiento import entenderAudio
from multiprocessing import Process,Pool,Queue,Value

from Variable_compartida import Variable_compartida
from Server_socket import ServerSocket

from sumar import sumarChimbita

# * --------------------------------------------------
# AJUSTES DEL SPEECH RECOGNITION
r = sr.Recognizer()
r.energy_threshold=4000
m = sr.Microphone(0,sample_rate=22050)

# Obtenemos el path actual del archivo main.py
current_path = pathlib.Path(__file__).parent
modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "DiosPadre-DiosHijo-DiosEspirituSanto.joblib")

# Se carga el modelo de red neuronal entrenado.
modelo_entrenado = joblib.load(modelo_ruta)
# * --------------------------------------------------

def start_recognizer(getter):
    while True:
        with m as source:
            try:
                print(f"EN START_RECOGNIZER APARECE EL VALOR DE {getter()} 👻" )
                print("Hable")
                audio = r.listen(source,phrase_time_limit=4) #,timeout=4
                palabra_predictor = entenderAudio(audio)
                predicion, = modelo_entrenado.predict(palabra_predictor)
                # y_prob = modelo_entrenado.predict_proba(palabra_predictor)
                if(predicion == 0):
                    desicion = "Empezar"
                elif(predicion == 1):
                    desicion = "Girar"
                elif(predicion == 2):
                    desicion = "Leprechaun"
                elif(predicion == 3):
                    desicion = "Mas"
                    # print("DIJO MÁS SAPO HPTA")
                    # pg.event.post(pg.K_RIGHT)
                elif(predicion == 4):
                    desicion = "Menos"
                else:
                    desicion = ""
                mi_socket = socket.socket()
                mi_socket.connect(("localhost",8001))
                # conexion,addr = mi_socket.accept()
                # mi_socket.send("Hola desde el cliente")
                # recibe 1024 bits
                mi_socket.send(desicion.encode())
                # print(respuesta.decode())
                app.saludar()
                mi_socket.close()
                # print(desicion)
                time.sleep(3)
            except Exception as e:
                print(f"Excepcion: {str(e)}")




class App():
    def __init__(self,valor_compartido):
        pg.init()
        pg.display.set_caption("Tetris - PDSA")
        self.screen = pg.display.set_mode(WIN_RES)    #Inicializa la ventana o pantalla a mostrar
        self.clock = pg.time.Clock()    # Crea un objeto que ayuda a llevar el tiempo
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.ultima_accion = {}
       
        # self.socket_py = socket.socket()
        # self.socket_py.connect(("localhost",8001))
        self.mi_variable =valor_compartido
        # print(self)
        # self.miTestSocketServer.attach(self)

    def get_mi_variable(self):
        return self.mi_variable

    def set_mi_Variable(self,nuevo_valor):
        self.mi_variable = nuevo_valor


    def saludar(self):
        print("makiavelico")  

    def load_images(self):
        # Obtenemos el path actual del archivo main.py
        current_path = pathlib.Path(__file__).parent
        # Guardamos la ruta donde se encuentran los sprites
        sprites_ruta = pathlib.Path(current_path / "assets" / "sprites")

        # Recorremos los archivos dentro de la carpeta de sprites y los guardamos en una variable "files"
        files = [item for item in sprites_ruta.rglob('*.png') if item.is_file()]
        # Cargamos las imágenes con un canal transparente para que el formato .png se vea con la transparencia que lo caracteria en cada uno de los archivos cargados.
        images = [pg.image.load(file).convert_alpha() for file in files]
        # Escalamos los sprites a los tamaños de las casillas
        images = [pg.transform.scale(image,(TILE_SIZE,TILE_SIZE)) for image in images]
        return images


    # Este método permite que el movimiento de estas no dependa de los fps    
    def set_timer(self):
        self.user_event = pg.USEREVENT +0
        self.fast_user_event = pg.USEREVENT +1
        self.leer_event = pg.USEREVENT+2
        self.escuchar_event = pg.USEREVENT+3

        self.anim_trigger = False
        self.fast_anim_trigger = False
        # time.set_timer(): crea repetidamente un evento en la cola de eventos. El primer parámetro es el evento y el segundo los milisegundos con los cuales aparecerá cada vez en la cola de eventos.
        pg.time.set_timer(self.user_event,ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event,FAST_ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.escuchar_event,4000)
        # pg.time.set_timer(self.leer_event,3500)


    def update(self):
        self.tetris.update()
        self.clock.tick(FPS) # Actualiza el objeto "clock"
        # print(get_shared_variable())

    def hola(self):
        print("HOLA BONITO")

    def draw(self):
        self.screen.fill(color=BG_COLOR) # Agregamos un color azul a la pantalla
        self.screen.fill(color=FIELD_COLOR,rect=(0,0,*FIELD_RES)) # Pintamos de gris únicamente las casillas jugables.
        self.tetris.draw()
        # Dibuja los textos en pantalla
        self.text.draw()
        pg.display.flip() # Actualiza todo el contenido mostrado en pantalla


    def check_events(self):
        # Esta propiedad va ligada al movimiento de las fichas. Permite que el movimiento de estas no dependa de los fps
        self.anim_trigger = False
        self.fast_anim_trigger = False
        # print(self.accion.getAccion_tomada())

        #pg.event(): obtiene los eventos de la cola de acciones por realizar
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
                pg.quit() # Desinicializa (termina) todos los módulos de Pygame
                sys.exit()
            elif event.type == self.escuchar_event:
                
                # a = self.get_mi_variable()
                # print(a)

                # b = a+1;
                # self.set_mi_Variable(b)
                # print(f"Valor después de sumar: {b}")
                print(f"DENTRO DE PYGAME, EL VALOR DE MI_VARIABLE ES: {self.mi_variable.getValue()}")
                pass
                # x =Value('i', 8)
                # proceso1 = Process(target=start_recognizer,args=(self.q,))
                # proceso1 = Process(target=start_recognizer)
                # proceso1.start()
                # print(f"En pygame: {mi_variable.getValue()}")
                # print("EN")
                # proceso1.join()
                # print("Acabó el proceso")
                # try:
                #     # print(len(self.q))
                #     print("Escuchar event")
                #     if(not self.q.empty()):
                #         print(self.q.get())
                #         print("Terminó")
                            
                #     print("Cola vacia")
                
                # except Exception as e:
                #     print(e)
                # accion = q.get()
                # # proceso1.start()
                # # proceso1.join()
                # print("Toma de desición")
                # # accion = start_recognizer()
                # if(accion == "Empezar"):
                #     print("EMPEZAR")
                # elif(accion == "Menos"):
                #     self.tetris.tetromino.move("left")
                # elif(accion == "Mas"):
                #     self.tetris.tetromino.move("right")
                # elif(accion == "Leprechaun"):
                #     print("Leprechaun")
                #     self.tetris.speed_up = True
                # elif(accion == "Girar"):
                #     print("GIRAR")
                #     self.tetris.tetromino.rotate()
                # print("Ya escogió la acción")
            
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger= True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger= True
       

    def run(self):
        
        
        while True:
            self.check_events();
            self.update();
            self.draw()
            # config_socket_server()
            # print(self.accion.accion_tomada)
            

# Ejecuta el archivo "main.py" principal como __main__ e inicializa el aplicativo.
# Evita que se ejecuten partes del código cuando se importan otros módulos en un mismo archivo.
if __name__ == "__main__":
    mi_variable_definitiva = Variable_compartida(3)
    print(mi_variable_definitiva.getValue())
    app = App(valor_compartido=mi_variable_definitiva)

    # app = App()
    proceso3 = Process(target=sumarChimbita,args=(mi_variable_definitiva.getValue,mi_variable_definitiva.setValue))
    proceso3.start()

    proceso1 = Process(target=start_recognizer,args=(mi_variable_definitiva.getValue,))
    proceso1.start()
    # miTestSocketServer = ServerSocket("test1",8001)
    # proceso2 = Process(target=miTestSocketServer.start_socket_server,args=(app.set_mi_Variable))
    # proceso2.start()
    
    
    # miTestSocketServer = ServerSocket("test1",8001)
    # miTestSocketServer.attach(app)

    # proceso2 = Process(target=miTestSocketServer.start_socket_server)
    # proceso2.start()
    app.run()
