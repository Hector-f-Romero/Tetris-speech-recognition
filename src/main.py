import speech_recognition as sr
from settings import *
from tetris import Tetris, Text
import sys
import pathlib
import time
import joblib
import pygame as pg
import json

from preprocesamiento import entenderAudio
from multiprocessing import Process, Pool, Queue, Value

# * --------------------------------------------------
# AJUSTES DEL SPEECH RECOGNITION
r = sr.Recognizer()
r.energy_threshold = 4000
m = sr.Microphone(0, sample_rate=44100)

# Obtenemos el path actual del archivo main.py
current_path = pathlib.Path(__file__).parent
modelo_ruta = pathlib.Path(current_path / "assets" /
                           "models" / "ModeloMakia1.joblib")

# Se carga el modelo de red neuronal entrenado.
modelo_entrenado = joblib.load(modelo_ruta)
# * --------------------------------------------------


def start_recognizer(q):
    while True:
        with m as source:
            try:
                print("Hable")
                # r.adjust_for_ambient_noise(source)
                # ,timeout=4,phrase_time_limit=5
                audio = r.listen(source, phrase_time_limit=3)
                palabra_predictor = entenderAudio(audio)
                predicion, = modelo_entrenado.predict(palabra_predictor)
                y_prob = modelo_entrenado.predict_proba(palabra_predictor)
                print(predicion)
                print(y_prob)
                desicion = ""
                if (predicion == 1):
                    desicion = "Empezar"
                elif (predicion == 2):
                    desicion = "Girar"
                elif (predicion == 3):
                    desicion = "Leprechaun"
                elif (predicion == 4):
                    desicion = "Mas"
                elif (predicion == 5):
                    desicion = "Menos"
                else:
                    desicion = ""

                q.put(desicion, block=False)

                time.sleep(1)
            except Exception as e:
                print(f"Excepcion: {str(e)}")


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetrisfán - PDSA")
        # Inicializa la ventana o pantalla a mostrar
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()    # Crea un objeto que ayuda a llevar el tiempo
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.ultima_accion = {}
        self.my_queue = Queue()

        proceso1 = Process(target=start_recognizer, args=(self.my_queue,))
        proceso1.start()

    def load_images(self):
        # Obtenemos el path actual del archivo main.py
        current_path = pathlib.Path(__file__).parent
        # Guardamos la ruta donde se encuentran los sprites
        sprites_ruta = pathlib.Path(current_path / "assets" / "sprites")

        # Recorremos los archivos dentro de la carpeta de sprites y los guardamos en una variable "files"
        files = [item for item in sprites_ruta.rglob(
            '*.png') if item.is_file()]
        # Cargamos las imágenes con un canal transparente para que el formato .png se vea con la transparencia que lo caracteria en cada uno de los archivos cargados.
        images = [pg.image.load(file).convert_alpha() for file in files]
        # Escalamos los sprites a los tamaños de las casillas
        images = [pg.transform.scale(
            image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    # Este método permite que el movimiento de estas no dependa de los fps

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.leer_event = pg.USEREVENT+2
        self.escuchar_event = pg.USEREVENT+3

        self.anim_trigger = False
        self.fast_anim_trigger = False
        # time.set_timer(): crea repetidamente un evento en la cola de eventos. El primer parámetro es el evento y el segundo los milisegundos con los cuales aparecerá cada vez en la cola de eventos.
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.escuchar_event, 4000)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)  # Actualiza el objeto "clock"
        # print(get_shared_variable())

    def draw(self):
        # Agregamos un color azul a la pantalla
        self.screen.fill(color=BG_COLOR)
        # Pintamos de gris únicamente las casillas jugables.
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        # Dibuja los textos en pantalla
        self.text.draw()
        pg.display.flip()  # Actualiza todo el contenido mostrado en pantalla

    def read_external_file(self):
        with open('json_data.json') as json_file:
            data = json.load(json_file)
            return data

    def check_events(self):
        # Esta propiedad va ligada al movimiento de las fichas. Permite que el movimiento de estas no dependa de los fps
        self.anim_trigger = False
        self.fast_anim_trigger = False
        # print(self.accion.getAccion_tomada())

        # pg.event(): obtiene los eventos de la cola de acciones por realizar
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
                pg.quit()  # Desinicializa (termina) todos los módulos de Pygame
                sys.exit()
            elif event.type == self.escuchar_event:
                try:
                    if (self.my_queue.empty()):
                        print("La cola está vacía.")
                        return
                    accion = self.my_queue.get(block=False)
                    print(accion)
                    if (accion == "Empezar"):
                        print("EMPEZAR")
                    elif (accion == "Menos"):
                        self.tetris.tetromino.move("left")
                    elif (accion == "Mas"):
                        self.tetris.tetromino.move("right")
                    elif (accion == "Leprechaun"):
                        print("Leprechaun")
                        self.tetris.speed_up = True
                    elif (accion == "Girar"):
                        print("GIRAR")
                        self.tetris.tetromino.rotate()
                    print("Ya escogió la acción")
                except Exception as e:
                    print(e)

            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            # print(self.accion.accion_tomada)


# Ejecuta el archivo "main.py" principal como __main__ e inicializa el aplicativo.
# Evita que se ejecuten partes del código cuando se importan otros módulos en un mismo archivo.
if __name__ == "__main__":
    app = App()
    app.run()
