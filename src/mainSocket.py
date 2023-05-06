import speech_recognition as sr
from settings import *
from tetris import Tetris, Text
import sys
import pathlib
import pygame as pg
import json
import socket

from preprocesamientoConv import entenderAudio
from multiprocessing import Process, Pool, Queue, Value


def socketConfig(q):
    my_socket = socket.socket()
    my_socket.bind(("localhost", 8000))
    my_socket.listen(5)
    print("Socket configurado 👻")
    try:
        while True:
            clientConnected, addr = my_socket.accept()
            respuesta = clientConnected.recv(1024)
            # print(respuesta.decode())
            q.put(respuesta.decode(), block=False)

    except Exception:
        print('interrupted!')


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

        proceso2 = Process(target=socketConfig, args=(self.my_queue,))
        proceso2.start()

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
        # time.set_timer(): crea repetidamente un evento en la cola de eventos. El primer parámetro es el evento y el segundo los milisegundos con los cuales aparecerá cada     vez en la cola de eventos.
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.escuchar_event, 100)

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
                    # pass
                    if (self.my_queue.empty()):
                        # print("La cola está vacía.")
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

                        self.tetris.speed_up = True

                    elif (accion == "Girar"):

                        self.tetris.tetromino.rotate()
                    else:
                        print("No se detectó la acción")

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


# Ejecuta el archivo "main.py" principal como __main__ e inicializa el aplicativo.
# Evita que se ejecuten partes del código cuando se importan otros módulos en un mismo archivo.
if __name__ == "__main__":
    app = App()
    app.run()
