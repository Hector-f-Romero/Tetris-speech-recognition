from settings import *
from tetris import Tetris
import sys

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Tetris - PDSA")
        self.screen = pg.display.set_mode(FIELD_RES)    #Inicializa la ventana o pantalla a mostrar
        self.clock = pg.time.Clock()    # Crea un objeto que ayuda a llevar el tiempo
        self.set_timer()
        self.tetris = Tetris(self)

    # Este método permite que el movimiento de estas no dependa de los fps    
    def set_timer(self):
        self.user_event = pg.USEREVENT +0
        self.anim_trigger = False
        # time.set_timer(): crea repetidamente un evento en la cola de eventos. El primer parámetro es el evento y el segundo los milisegundos con los cuales aparecerá cada vez en la cola de eventos.
        pg.time.set_timer(self.user_event,ANIM_TIME_INTERVAL)
    
    def update(self):
        self.tetris.update()
        self.clock.tick(FPS) # Actualiza el objeto "clock"

    def draw(self):
        self.screen.fill(color=FIELD_COLOR)
        self.tetris.draw()
        pg.display.flip() # Actualiza todo el contenido mostrado en pantalla

    def check_events(self):
        # Esta propiedad va ligada al movimiento de las fichas. Permite que el movimiento de estas no dependa de los fps
        self.anim_trigger = False
        #pg.event(): obtiene los eventos de la cola de acciones por realizar
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
                pg.quit() # Desinicializa (termina) todos los módulos de Pygame
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger= True
    def run(self):
        while True:
            self.check_events();
            self.update();
            self.draw()

# Ejecuta el archivo "main.py" principal como __main__ e inicializa el aplicativo.
# Evita que se ejecuten partes del código cuando se importan otros módulos en un mismo archivo.
if __name__ == "__main__":
    app = App()
    app.run()
