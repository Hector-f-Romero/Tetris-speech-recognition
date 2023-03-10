from settings import *
from tetromino import Tetromino
import math

# La clase Tetris llevará el control de los elemtentos Tetromino y la visualización en pantalla de la grilla
class Tetris:
    def __init__(self,app):
        self.app =app
        # En este group, estarán todas las texturas de los Tetrominos y bloques que aparecerán en pantalla
        self.sprite_group = pg.sprite.Group()
        self.tetromino = Tetromino(self)

    # Dibuja la cuadrícula en pantalla con base en los ajustes del archivo "settings"
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen,"black",(x*TITLE_SIZE,y*TITLE_SIZE,TITLE_SIZE,TITLE_SIZE),1)
    
    def update(self):
        self.tetromino.update()
        self.sprite_group.update()

    def draw(self):
       self.draw_grid()
       # Dibujará los sprites en la superficie de la pantalla de la aplicación previamente creada.
       self.sprite_group.draw(self.app.screen) 