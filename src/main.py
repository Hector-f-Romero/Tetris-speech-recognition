from settings import *
from tetris import Tetris,Text
import sys
import pathlib

# from shared_variable import get_shared_variable
from accionTomada import VariableCompartida
from speechRecognition import start_recognizer
from multiprocessing import Process,Pool,Queue,Value

mi_accion = VariableCompartida()

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris - PDSA")
        self.screen = pg.display.set_mode(WIN_RES)    #Inicializa la ventana o pantalla a mostrar
        self.clock = pg.time.Clock()    # Crea un objeto que ayuda a llevar el tiempo
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        proceso1 = Process(target=start_recognizer)
        proceso1.start()


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
        self.anim_trigger = False
        self.fast_anim_trigger = False
        # time.set_timer(): crea repetidamente un evento en la cola de eventos. El primer parámetro es el evento y el segundo los milisegundos con los cuales aparecerá cada vez en la cola de eventos.
        pg.time.set_timer(self.user_event,ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event,FAST_ANIM_TIME_INTERVAL)
    
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
        #pg.event(): obtiene los eventos de la cola de acciones por realizar
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
                pg.quit() # Desinicializa (termina) todos los módulos de Pygame
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger= True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger= True
        # print(get_shared_variable())
        # print(mi_accion)
        # mi_accion.obtener_valor()
        if(mi_accion.obtener_valor()==4):
            print("Menos")
            # print(get_shared_variable())
            # self.tetris.tetromino.move(direction="left")
        elif (mi_accion.obtener_valor()==3):
            print("Mas")
            # self.tetris.tetromino.move(direction="right")
        elif (mi_accion.obtener_valor()==0):
            # print("Empezar en main")
            print(mi_accion)
            # print(get_shared_variable())
            # self.tetris.tetromino.move(direction="right")
        print(mi_accion.obtener_valor())

        
    def run(self):
        while True:
            self.check_events();
            self.update();
            self.draw()

# Ejecuta el archivo "main.py" principal como __main__ e inicializa el aplicativo.
# Evita que se ejecuten partes del código cuando se importan otros módulos en un mismo archivo.
if __name__ == "__main__":
    app = App()
    # proceso1 = Process(target=start_recognizer)
    # proceso1.start() 
      
    # p = Pool(processes=3)
    # dato = p.map(start_recognizer)
    # p.close()
    # print(dato)
    app.run()
    # start_recognizer()
