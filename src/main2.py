import speech_recognition as sr
from settings import *
from tetris import Tetris,Text
import sys
import pathlib
import time
import joblib
import pygame as pg
import json

# from shared_variable import get_shared_variable
# from shared_variable import VariableCompartida
# from speechRecognition import start_recognizer
from preprocesamiento import entenderAudio
from multiprocessing import Process,Pool,Queue,Value
import queue
from accionTomada import AccionTomada

# * --------------------------------------------------
# AJUSTES DEL SPEECH RECOGNITION
r = sr.Recognizer()
r.energy_threshold=4000
m = sr.Microphone(0,sample_rate=44000)

# Obtenemos el path actual del archivo main.py
current_path = pathlib.Path(__file__).parent
# modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "Model081.joblib")
# modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "my_random_forest.joblib")
modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "Model082palabramasperfecta.joblib")


# Se carga el modelo de red neuronal entrenado.
modelo_entrenado = joblib.load(modelo_ruta)

# * --------------------------------------------------
# mi_accion = queue.Queue()

def start_recognizer2():
    while True:
        with m as source:
            try:
                print("Hable")
                audio = r.listen(source,phrase_time_limit=2,timeout=1.5) #,
                palabra_predictor = entenderAudio(audio)
                predicion, = modelo_entrenado.predict(palabra_predictor)
                y_prob = modelo_entrenado.predict_proba(palabra_predictor)
                # accion.setAccion_tomada(predicion)
                # print(predicion)
                # print(accion.getAccion_tomada())
                # with open("audio_file.wav", "wb") as file:
                desicion = ""
                # print(predicion)
                if(predicion == 0):
                    desicion = "Empezar"
                elif(predicion == 1):
                    desicion = "Girar"
                elif(predicion == 2):
                    desicion = "Leprechaun"
                elif(predicion == 3):
                    desicion = "Más"
                elif(predicion == 4):
                    desicion = "Menos"
                elif(predicion == 5):
                    desicion = "Soltar"
                else:
                    desicion = ""
                
                data = {
                    "id":str(predicion),
                    "accion":desicion
                }
                json_string = json.dumps(data)
                with open('json_data.json', 'w') as outfile:
                    outfile.write(json_string)
                print("-----------------------------------------------")
                time.sleep(2)
            except Exception as e:
                print(f"Excepcion: {str(e)}")

def leerJSON():
        with open('json_data.json') as json_file:
            data = json.load(json_file)
            
            print(data)
            return data
            # time.sleep(5)

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris - PDSA")
        self.screen = pg.display.set_mode(WIN_RES)    #Inicializa la ventana o pantalla a mostrar
        self.clock = pg.time.Clock()    # Crea un objeto que ayuda a llevar el tiempo
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.limpiarJSON()
        self.text = Text(self)
        self.ultima_accion = {}
        self.i = 0

        proceso1 = Process(target=start_recognizer2)
        # proceso2 = Process(target=leerJSON,args=(self.ultima_accion,))
        proceso1.start()
        # proceso2.start()
        # proceso1.join()

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
        # pg.time.set_timer(self.escuchar_event,4000)
        pg.time.set_timer(self.leer_event,3500)
    
    def update(self):
        self.tetris.update()
        self.clock.tick(FPS) # Actualiza el objeto "clock"
        # print(get_shared_variable())

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
            elif event.type==self.leer_event:
                with open('json_data.json') as json_file:
                    data = json.load(json_file)
                    if(data =={}):
                        return
                    print(data)
                    accion = data["accion"]
                    # accion = dataaccion
                    if(accion == "Empezar"):
                        print("EMPEZAR")
                    elif(accion == "Menos"):
                        self.tetris.tetromino.move("left")
                    elif(accion == "Más"):
                        self.tetris.tetromino.move("right")
                    elif(accion == "Soltar"):
                        print("SOLTAR")
                        self.tetris.speed_up = True
                    elif(accion == "Girar"):
                        print("GIRAR")
                        self.tetris.tetromino.rotate()
            elif event.type == self.escuchar_event:
                start_recognizer2()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger= True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger= True

    
       
    def limpiarJSON(self):
        # Abre el archivo en modo escritura
        with open('json_data.json', 'w') as archivo:
            # Utiliza la función truncate() para sobrescribir el contenido del archivo
            archivo.truncate()

        # Crea un diccionario vacío en Python
        data = {}

        # Agrega el diccionario vacío al archivo JSON
        with open('json_data.json', 'w') as archivo:
            json.dump({}, archivo)
                
    
    def run(self):
        while True:
            self.check_events();
            self.update();
            self.draw()
            # print(self.accion.accion_tomada)
            

# Ejecuta el archivo "main.py" principal como __main__ e inicializa el aplicativo.
# Evita que se ejecuten partes del código cuando se importan otros módulos en un mismo archivo.
if __name__ == "__main__":
    app = App()
    
    app.run()
